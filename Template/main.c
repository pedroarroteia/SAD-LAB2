#include <p24fxxxx.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

// Configuration Bits
#ifdef __PIC24FJ64GA004__ //Defined by MPLAB when using 24FJ64GA004 device
_CONFIG1( JTAGEN_OFF & GCP_OFF & GWRP_OFF & COE_OFF & FWDTEN_OFF & ICS_PGx1 & IOL1WAY_ON) 
_CONFIG2( FCKSM_CSDCMD & OSCIOFNC_OFF & POSCMOD_HS & FNOSC_PRI & I2C1SEL_SEC)
#else
_CONFIG1( JTAGEN_OFF & GCP_OFF & GWRP_OFF & COE_OFF & FWDTEN_OFF & ICS_PGx2) 
_CONFIG2( FCKSM_CSDCMD & OSCIOFNC_OFF & POSCMOD_HS & FNOSC_PRI)
#endif

//U2MODE: UARTx Mode Register
//U2RXREG: UARTx Receive Register
//U2STA: UARTx Status and Control Register
//U2TXREG: UARTx Transmit Register (Write-Only) 
//U2BRG: UARTx Baud Rate Generator Register

	int i = 0;
	//int index_Uart=0;
	int independentChannel = 1;
	int actvAlert = 0;
	int ADCValue;
	int controloFlagUART = 0;
	
	//vetores para guardar strings
	char receivestring[100];
	
	//vetores para guardar amostras
	int AN0[5];
	int AN4[5];
	int AN5[5];
	int B7[5];
	int D6[5];
	int D7[5];	

	//Limite dos contadores
	int counterTimeoutAN0 = -1;
	int counterTimeoutAN4 = -1;
	int counterTimeoutAN5 = -1;
	int counterTimeoutB7 = -1;
	int counterTimeoutD6 = -1;
	int counterTimeoutD7 = -1;
	
	//contadores
	int counterTimerAN0 = 0;
	int counterTimerAN4 = 0;
	int counterTimerAN5 = 0;
	int counterTimerB7 = 0;
	int counterTimerD6 = 0;
	int counterTimerD7 = 0;
	
	//Limite do numero de amostras
	int counterNumOutAN0 = 1;
	int counterNumOutAN4 = 1;
	int counterNumOutAN5 = 1;
	int counterNumOutB7 = 1;
	int counterNumOutD6 = 1;
	int counterNumOutD7 = 1;	
	
	//numero de amostras
	int counterNumAN0 = 0;
	int counterNumAN4 = 0;
	int counterNumAN5 = 0;
	int counterNumB7 = 0;
	int counterNumD6 = 0;
	int counterNumD7 = 0;

	int receiveFromArduino = 0;

//////////////////////////////////////////Delay Function///////////////////////////////////////////
//
	void Delay(unsigned int iter){
		for( i = 0 ; i < iter ; i++){};
	}
//	

//
//////////////////////////////////////////Transmition Functions///////////////////////////////////////////
//
	void TransmitChar(char data){
		while(U2STAbits.UTXBF == 1){} //while transmiter buffer is full. wait
		U2TXREG = data;  //transmitir data para o resgisto de transmis�o	
	}
	
	void TransmitString(char* string){
		for( i=0;string[i]!='\0';i++){ //Envia uma string caracter a caracter
			TransmitChar(string[i]);  //transmitir string 
		}
	}
		
//////////////////////////////////////////Initial Configuration Functions/////////////////////////////////
//
	void UART_config(){
		U2BRG = 12; // Baud rate = 19200; FCy=Fosc/2=8M/2=4M; UxBRG =12 
		U2MODE =  0x8000;	//Enable Uart for 8-bit data
		U2STA = 0x0400;		 	
	}	
	
	void ADC_config(){
		AD1PCFG = 0xFFCA; // AN0 AN2 AN4 and AN5 as analog, all other pins are digital
		AD1CON1 = 0x0000; // SAMP bit = 0 ends sampling and starts converting
		AD1CHS = 0x0005; // Connect AN5 as S/H+ input
		AD1CSSL = 0;
		AD1CON3 = 0x0002; // Manual Sample, Tad = 3Tcy
		AD1CON2 = 0;
		AD1CON1bits.ADON = 1; // turn ADC ON
	}

	void button_config(){	
		TRISDbits.TRISD6 = 1; //button 6 (1 means input)//active low
		TRISDbits.TRISD7 = 1; //button 7 (1 means input)//active low	
	}
	
	void led_config(){	
		TRISAbits.TRISA0 = 0; //Led 0 (0 means output)
		TRISAbits.TRISA1 = 0; //Led 1 (0 means output)
		TRISAbits.TRISA4 = 0; //Led 4 (0 means output)
	}
	void start_timer(){
		T1CON = 0x00; //Stops the Timer1 and reset control reg.
		TMR1 = 0x00; //Clear contents of the timer register
		PR1 = 0x0FA0; //Load the Period register with the value 0x0FA0
		IPC0bits.T1IP = 0x01; //Setup Timer1 interrupt for desired priority level
		IFS0bits.T1IF = 0; //Clear the Timer1 interrupt status flag
		IEC0bits.T1IE = 1; //Enable Timer1 interrupts
		T1CONbits.TON = 1; //Start Timer1 with prescaler settings at 1:1 and 
	}
	
	void configuration(){
					  
		ADC_config();
		UART_config();
		button_config();
		led_config();
		TRISAbits.TRISA7 = 0; //Bidirecional (0 - output, 1 - input)
	
		I2C2BRG = 0x27;
		I2C2CON = 0x8000;
		
		IEC1bits.U2RXIE = 1; //Ativa��o interrupt UART
		Delay(2);
		start_timer();
	
	}
	

//
//////////////////////////////////////////	I2C	///////////////////////////////////////////
//	
		
	void i2cProtocolWrite(int SlaveAdd, int data){	
	
		
		I2C2CONbits.SEN = 1;
		while(I2C2CONbits.SEN){} //start
			
		I2C2TRN = ((SlaveAdd << 1) + 0); //write = 0; envia o endere�o do slave
		while(I2C2STATbits.TBF){} //transmit in progress
		while(I2C2STATbits.TRSTAT){} //master transmit in progress
		if (I2C2STATbits.ACKSTAT == 0){
			//TransmitString("ack1\n\r");
		}

		I2C2TRN = data;
	    while(I2C2STATbits.TBF){} //transmit in progress
		while(I2C2STATbits.TRSTAT){} //master transmit in progress
		if (I2C2STATbits.ACKSTAT == 0){
			//TransmitString("ack2\n\r");
		}
		
		I2C2CONbits.PEN = 1;
		while(I2C2CONbits.PEN){}//stop	
		
	}
	
	
	void i2cProtocolRead(int SlaveAdd, int * val){	
	
		int b1 = 0,b2 = 0;
	
		
		I2C2CONbits.SEN = 1;
		while(I2C2CONbits.SEN){}//start
		
		//send device adress
		I2C2TRN = (SlaveAdd << 1) + 1; //read=1
		while(I2C2STATbits.TBF){} //transmit in progress
		while(I2C2STATbits.TRSTAT){} //master transmit in progress
		if (I2C2STATbits.ACKSTAT == 0){
		}
		
		//primeira rece��o
		I2C2CONbits.RCEN = 1;
		while(I2C2CONbits.RCEN == 1);
		val[0] = I2C2RCV;// guardar a informa��o rcebida em data
		I2C2CONbits.ACKDT = 0;//send ack
		I2C2CONbits.ACKEN = 1;//
		while(I2C2CONbits.ACKEN == 1);//initiate ack sequence	
		
		//segunda rece��o
		I2C2CONbits.RCEN = 1;//receive eneble
		while(I2C2CONbits.RCEN == 1);// while receive is not complete
		b1 = I2C2RCV;// guardar a informa��o rcebida em data
		I2C2CONbits.ACKDT = 0;//send ack
		I2C2CONbits.ACKEN = 1;// initiate ack sequence
		while(I2C2CONbits.ACKEN == 1);//initiate ack sequence
		
		//terceira rece��o
		I2C2CONbits.RCEN = 1;//receive eneble
		while(I2C2CONbits.RCEN == 1);// while receive is not complete
		b2 = I2C2RCV;// guardar a informa��o rcebida em data
		I2C2CONbits.ACKDT = 0;//send ack
		I2C2CONbits.ACKEN = 1;// initiate ack sequence
		while(I2C2CONbits.ACKEN ==1);//initiate ack sequence
		
		
		val[1] = b1 << 8 | b2;

		
		//quarta rece��o
		I2C2CONbits.RCEN = 1;//receive eneble
		while(I2C2CONbits.RCEN == 1);// while receive is not complete
		b1 = I2C2RCV;// guardar a informa��o rcebida em data
		I2C2CONbits.ACKDT = 0;//send ack
		I2C2CONbits.ACKEN = 1;// initiate ack sequence
		while(I2C2CONbits.ACKEN == 1);//
		
		//quinta rece��o
		I2C2CONbits.RCEN = 1;//receive eneble
		while(I2C2CONbits.RCEN == 1);// while receive is not complete
		b2 = I2C2RCV;// guardar a informa��o rcebida em data
		I2C2CONbits.ACKDT = 1;//send Nack
		I2C2CONbits.ACKEN = 1;// initiate ack sequence
		while(I2C2CONbits.ACKEN == 1);//initiate ack sequence
		
		I2C2CONbits.PEN = 1;
		while(I2C2CONbits.PEN){} //stop	
		
		val[2] = b1 << 8 | b2;
	}

//	
//////////////////////////////////////////Analog Channels Functions///////////////////////////////////////////	
//
	int ADC_read(int channel){	
		AD1CHS = channel; // Connect channel as S/H+ input
		AD1CON1bits.SAMP = 1; // start sampling
		Delay(1);
		AD1CON1bits.SAMP = 0; // start converting
		while (!AD1CON1bits.DONE){}; // wait for the conversion to be done		
		ADCValue = ADC1BUF0;
		return ADCValue;
	}	
	
	void transmitGEN(char* nomen, int counterNumAN, int* AN_val, char*str){

	
		if(counterNumAN>1){
			sprintf(str,"%s\"%s\":[",str, nomen);
		
			int j = 0;
			
			while(1){				
				if(j ==(counterNumAN-1)){
					sprintf(str,"%s%d]",str, AN_val[j]);
					break;
				}
				else{
					sprintf(str,"%s%d, ",str, AN_val[j]);
				}
				j++;
			}	
		}
		else{

			sprintf(str,"%s\"%s\": %i",str, nomen, AN_val[0]);
	    
		}
	    
	}

	void transmitALL(int ctrAN0, int* AN0, int ctrAN4, int* AN4, int ctrAN5, int* AN5, int ctrD6, int* D6, int ctrD7, int* D7, int ctrB7, int* B7, int receiveFromArduino, int* I2CVal0 , int* I2CVal1, int* I2CVal2){
	    char str[150];

		Delay(1);
	    sprintf(str, "{");
		Delay(1);
		
		if( (ctrAN0 || ctrAN4 || ctrAN5 || ctrD6 || ctrD7 || ctrB7 || receiveFromArduino)){
			if(ctrAN0){
				transmitGEN("AN0", counterNumOutAN0, AN0, str);
			
				if(ctrAN4 || ctrAN5 || ctrD6 || ctrD7 || ctrB7 || receiveFromArduino)
					sprintf(str, "%s,", str);
			}
				
			if(ctrAN4){
				transmitGEN("AN4", counterNumOutAN4, AN4, str);
				if(ctrAN5 || ctrD6 || ctrD7 || ctrB7 || receiveFromArduino)
					sprintf(str, "%s,", str);
			}
				
			
			if(ctrAN5){
				transmitGEN("AN5", counterNumOutAN5, AN5, str);
				if(ctrD6 || ctrD7 || ctrB7 || receiveFromArduino)
					sprintf(str, "%s,", str);
		
			}
				
			if(ctrD6){
				transmitGEN("D6", counterNumOutD6, D6, str);
				if(ctrD7 || ctrB7 || receiveFromArduino)
					sprintf(str, "%s,", str);
			}
				
			if(ctrD7){
				transmitGEN("D7", counterNumOutD7, D7, str);
				if(ctrB7 || receiveFromArduino)
					sprintf(str, "%s,", str);
			}
				
			if(ctrB7){
	
				transmitGEN("B7", counterNumOutB7, B7, str);
				if(receiveFromArduino)
					sprintf(str, "%s,", str);
			}
	
			if(receiveFromArduino){
				transmitGEN("Status", 1, I2CVal0, str);
				sprintf(str, "%s,", str);
	
				transmitGEN("sensor1", 1, I2CVal1, str);
				sprintf(str, "%s,", str);
	
				transmitGEN("sensor2", 1, I2CVal2, str);
			
			}
					
			Delay(1);
			sprintf(str, "%s}\n", str);
			Delay(1);
			TransmitString(str);
		}
	}


	void sampleConfig_rate(int sampleRate, int channel){
					
				counterTimerAN0 = 0;
				counterTimerAN4 = 0;
				counterTimerAN5 = 0;
				counterTimerB7 = 0;
				counterTimerD6 = 0;
				counterTimerD7 = 0;
				if (channel == 0){
					
					counterTimeoutAN0 = sampleRate;				
				}
				
				if (channel == 4){
					
					counterTimeoutAN4 = sampleRate;
					
				}
				
				if (channel == 5){
					counterTimeoutAN5 = sampleRate;
				}
				
	}
	
	void sampleDesactivate(int channel){
		
				if (channel == 0){
					counterTimeoutAN0 = -1;
				}
				
				if (channel == 4){
					counterTimeoutAN4 = -1;
				}
				
				if (channel == 5){
					counterTimeoutAN5 = -1;
				}
				
	}

	void sampleConfig_number(int num, int channel){


			if (channel == 0){
				counterNumAN0 = 0;
				counterNumOutAN0 = num;
			}
			if (channel == 4){
				counterNumOutAN4 = num;
				counterNumAN4 = 0;
			}
			
			if (channel == 5){
				counterNumOutAN5 = num;
				counterNumAN5 = 0;
			}
			
}
//
//////////////////////////////////////////Digital Channels Functions///////////////////////////////////////////
//	




	void sampleConfig_rate_digital(int sampleRate, int channel){
			counterTimerAN0 = 0;
			counterTimerAN4 = 0;
			counterTimerAN5 = 0;
			counterTimerB7 = 0;
			counterTimerD6 = 0;
			counterTimerD7 = 0;

			if (channel == 1){
				counterTimeoutB7 = sampleRate;		
			}
			if (channel == 6){
				counterTimeoutD6 = sampleRate;			
			}
			if (channel == 7){
				counterTimeoutD7 = sampleRate;
				
			}
			
			
	}

	void sampleDesactivate_digital(int channel){
	
			if (channel == 1){
				counterTimeoutB7 = -1;
			}
			if (channel == 6){
				counterTimeoutD6 = -1;
			}
			if (channel == 7){
				counterTimeoutD7 = -1;
			}
	}

	void sampleConfig_number_digital(int num, int channel){
	
			if (channel == 1){
				counterNumOutB7 = num;
				counterNumB7 = 0;
			
			}
			if (channel == 6){
				counterNumOutD6 = num;
				counterNumD6 = 0;
			
			}
			if (channel == 7){
				counterNumOutD7 = num;
				counterNumD7 = 0;
			
			}
			
	}
	void config_digital_io(int channel, int io_dir){
		
		if(channel == 1 )
			TRISAbits.TRISA7 = io_dir; //(0 - output, 1 - input)
	}
	
	int buttonRead(){
			if(independentChannel == 0)
				return (PORTDbits.RD7* pow(2,1))+(PORTDbits.RD6* pow(2,0));
			else 
				return -1;
	}
//
/////////////////////////////////////////////////////////Led functions	////////////////////////
//
	void led_enable(int led){
		if(led == 0)
			PORTAbits.RA0 = 1;
		if(led == 1)
			PORTAbits.RA1 = 1;
		if(led == 4)
			PORTAbits.RA4 = 1;
	}
	
	void led_disable(int led){
		if(led == 0)
			PORTAbits.RA0 = 0;
		if(led == 1)
			PORTAbits.RA1 = 0;
		if(led == 4)
			PORTAbits.RA4 = 0;
	}


	

//
///////////////////////////////////////Atribute functions////////////////////////////////
//


	int numSampleCheckAnalog(int* counterNum, int counterNumOut) {
		if (counterNumOut == counterNum[0]) {
			counterNum[0] = 0;
			return 1;
		}
		return 0;
	}

	void samplingPeriodCounterAnalog(int channel, int * vector, int * counterTimer,int counterTimeout, int * counterNum ){
		if(counterTimeout == counterTimer[0]){
			
			
			vector[counterNum[0]++] = ADC_read(channel);
			counterTimer[0] = 0; // por seguran�a meto aqui mas deveria dar em cima tamb�m, se n�o for o caso � porque  ele passou uma amostra a frente
		}

	}

	



	void samplingPeriodCounterDigital(int channel, int * vector,int value, int * counterTimer,int counterTimeout, int * counterNum){
		if(counterTimeout == counterTimer[0]){
				vector[counterNum[0]] = value;
				counterNum[0]++;
				counterTimer[0] = 0;
		}
	}

	void  __attribute__((__interrupt__, __shadow__)) _T1Interrupt(void){	
		
		counterTimerAN0++;
		if (counterTimerAN0 < 0) {// se o contador chegar ao valor maximo entra em overflow e passa para um numero negativo em binario

			counterTimerAN0 = 0;
		}
		counterTimerAN4++;
		if (counterTimerAN4 < 0) {// se o contador chegar ao valor maximo entra em overflow e passa para um numero negativo em binario

			counterTimerAN4 = 0;
		}
		counterTimerAN5++;
		if (counterTimerAN5 < 0) {// se o contador chegar ao valor maximo entra em overflow e passa para um numero negativo em binario

			counterTimerAN5 = 0;
		}
		counterTimerD6++;
		if (counterTimerD6 < 0) {// se o contador chegar ao valor maximo entra em overflow e passa para um numero negativo em binario

			counterTimerD6 = 0;
		}
		counterTimerD7++;
		if(counterTimerD7  < 0){// se o contador chegar ao valor maximo entra em overflow e passa para um numero negativo em binario
	        	
			counterTimerD7 = 0;
		}
		
		
		if (TRISAbits.TRISA7 == 1) { //se etiver em modo input
			counterTimerB7++;
			if (counterTimerB7 < 0) {// se o contador chegar ao valor maximo entra em overflow e passa para um numero negativo em binario
				counterTimerB7 = 0;
			}
		}	
		
		if(actvAlert == buttonRead())
			TransmitString("Alerta - Detecao no Canal Virtual "); //trocar por variavel de controlo e por este transmit no main, mas se puser no main perde um pouco o proposito
			

		IFS0bits.T1IF = 0; //Reset Timer1 interrupt flag and Return from ISR
	}


	void  __attribute__((__interrupt__,no_auto_psv)) _U2RXInterrupt(void){
		controloFlagUART=1;
		
		IFS1bits.U2RXIF = 0; //Reset interrupt flag and Return from ISR
	}
	
//	
//////////////////////////////////////////Receive Functions///////////////////////////////////////////
//
	char ReceiveChar(){
		while(U2STAbits.URXDA == 0){} //while receiver buffer is empty. wait.
		return U2RXREG; //receber data do resgisto de rece��o
	}
	
			
	int convert_string_int(char * str, int lenArg) {
		int sum = 0;
		int n = 0;
		int i = 0;
		int number;
		
		for (n = lenArg - 1, i = 0; n >= 0; n--, i++) {			
			number = ((int)str[i] - 48);
			sum = sum + number *pow(10,n);	
		}
			
		return sum;
	}
//
	void ReceiveString(){

		receivestring[0]=ReceiveChar();		
		int i=1;
		

		while(1){ 
			receivestring[i] = ReceiveChar();   
			if(receivestring[i]=='}'){
				break;
			}
			i++;
		}
		receivestring[i+2]= '\0';

		
	}
	
	void interpretadorJson(){
		int n = 0;
		char json[20];
		char argJson_aux[20];
		int argJson[20];
		int controlJson1 = 0;
		int controlJson2 = 0;
		int controlJson3 = 0;
		int controlJson4 = 0;
		int controlJson5 = 0;
		
		
		while(1){ 

			if('"' == receivestring[n]){
				controlJson3++;
				controlJson1 = 0;
			}
			else if('[' ==  receivestring[n]){
				controlJson4 = 1;
				controlJson2 = 0;
				controlJson5 = 0;
			}
			else if(']' ==  receivestring[n]){
				controlJson4 = 0;
				
			
			
				if((strcmp(json,"analogAmostragem")==0) && (argJson[1] == 1)){
					sampleConfig_rate(1000, argJson[0]);
				
				}
				else if((strcmp(json,"analogAmostragem")==0) && (argJson[1] == 0)){
					sampleDesactivate(argJson[0]);
				}

				else if(strcmp(json,"freqAmostragem")==0){
					sampleConfig_rate(argJson[1], argJson[0]);
				}
				else if(strcmp(json,"numAmostragem")==0){
					sampleConfig_number(argJson[1], argJson[0]);
				}
				else if(strcmp(json,"Bidirecional")==0){
					config_digital_io(argJson[0], argJson[1]);
				}
				else if((strcmp(json,"DigitalAmostragem")==0) && (argJson[1] == 1) ){
					sampleConfig_rate_digital(1000, argJson[0]);
				}
				else if((strcmp(json,"DigitalAmostragem")==0)  && (argJson[1] == 0)){
					sampleDesactivate_digital(argJson[0]);
				}
				
				else if(strcmp(json,"DigitalFreq")==0){
					sampleConfig_rate_digital(argJson[1], argJson[0]);
				}
				else if(strcmp(json,"DigitalNum")==0){
					sampleConfig_number_digital(argJson[1], argJson[0]);
				}
				else if(strcmp(json,"virtual")==0){
					independentChannel = argJson[0];
				}
				else if(strcmp(json,"alertEvent")==0){			
					actvAlert = argJson[0];
				}
				else if((strcmp(json,"Led")==0) && (argJson[1] == 1)){
						led_enable(argJson[0]);
				}
				else if((strcmp(json,"Led")==0) && (argJson[1] == 0)){
					led_disable(argJson[0]);
				}				
				else if((strcmp(json,"BidirecionalActive")==0) && (TRISAbits.TRISA7 == 0)){  
					PORTAbits.RA7 = 1;
					Delay(1000);
					PORTAbits.RA7 = 0;
					
				}
				else if((strcmp(json,"I2C")==0)){  
					receiveFromArduino = 1;	
				}	
			}
			else if ((' ' == receivestring[n]) || (':' == receivestring[n]) || (',' == receivestring[n] && controlJson4 == 0)){} 
			else{
	
				if( (controlJson3%2) == 1  ){
					json[controlJson1++] = receivestring[n];
					json[controlJson1] = '\0';
				}
				else if(controlJson4 == 1){
					if(receivestring[n] != ',' )
						argJson_aux[controlJson2++] = receivestring[n];
					else {
						argJson[controlJson5++] = convert_string_int(argJson_aux, controlJson2);
						controlJson2 = 0;
					}
					if(receivestring[n + 1] == ']'){
						argJson[controlJson5++] = convert_string_int(argJson_aux, controlJson2);
						controlJson2 = 0;
					}
				}
			}
			// Fechar o intrepertador
			if(receivestring[n] == '}'){
				break;
			}
			n++;			
		}			
	}
	
	
	
	
	

//	
//////////////////////////////////////////MAIN///////////////////////////////////////////
//
	int main(void){
		int I2CVal[3]; 
		int ctrAN0 = 0;
		int ctrAN4 = 0;
		int ctrAN5 = 0;
		int ctrD6 = 0;
		int ctrD7 = 0;
		int ctrB7 = 0;
		configuration();
	
		while ( 1 ){
			
		

			if(controloFlagUART == 1){
				ReceiveString();
				interpretadorJson();
				controloFlagUART = 0;
			}	
		
			samplingPeriodCounterAnalog( 0, AN0, &counterTimerAN0, counterTimeoutAN0, &counterNumAN0);
			samplingPeriodCounterAnalog( 4, AN4, &counterTimerAN4, counterTimeoutAN4, &counterNumAN4);
			samplingPeriodCounterAnalog( 5, AN5, &counterTimerAN5, counterTimeoutAN5, &counterNumAN5);
			samplingPeriodCounterDigital(6,  D6,    PORTDbits.RD6,   &counterTimerD6, counterTimeoutD6, &counterNumD6);
			samplingPeriodCounterDigital(7,  D7,    PORTDbits.RD7,   &counterTimerD7, counterTimeoutD7, &counterNumD7 );
			samplingPeriodCounterDigital(1,  B7,    PORTAbits.RA7,   &counterTimerB7, counterTimeoutB7, &counterNumB7);


			ctrAN0 = numSampleCheckAnalog( &counterNumAN0, counterNumOutAN0);
			ctrAN4 = numSampleCheckAnalog(&counterNumAN4, counterNumOutAN4);
			ctrAN5 = numSampleCheckAnalog(&counterNumAN5, counterNumOutAN5);
			ctrD6 = numSampleCheckAnalog(&counterNumD6, counterNumOutD6);
			ctrD7 = numSampleCheckAnalog(&counterNumD7, counterNumOutD7);
			ctrB7 = numSampleCheckAnalog(&counterNumB7, counterNumOutB7);

			

			if(receiveFromArduino){
				i2cProtocolWrite(0x48, 0xAC);
				i2cProtocolRead(0x48, I2CVal);
			}
	
			
			
			
			transmitALL(ctrAN0, AN0, ctrAN4, AN4, ctrAN5, AN5, ctrD6, D6, ctrD7, D7, ctrB7, B7, receiveFromArduino, &I2CVal[0] , &I2CVal[1], &I2CVal[2]);
			receiveFromArduino = 0;
			ctrAN0 = 0;
			ctrAN4 = 0;
			ctrAN5 = 0;
			ctrD6 = 0;
			ctrD7 = 0;
			ctrB7 = 0;
						
		}
		
	}
