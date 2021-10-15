void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);    // sets the digital pin 13 as output
}

void loop() {

  //sets high
  digitalWrite(13, HIGH);
  _sw_uart_wait_T();

  //starts transmission
  digitalWrite(13, LOW); 
  _sw_uart_wait_T();

  //sending bytes
  digitalWrite(13, LOW); 
  _sw_uart_wait_T();

  digitalWrite(13, LOW);
  _sw_uart_wait_T();

  digitalWrite(13, LOW); 
  _sw_uart_wait_T();

  digitalWrite(13, LOW);
  _sw_uart_wait_T();

  digitalWrite(13, HIGH);
  _sw_uart_wait_T();

  digitalWrite(13, LOW); 
  _sw_uart_wait_T();

  digitalWrite(13, HIGH);
  _sw_uart_wait_T();

  digitalWrite(13, LOW); 
  _sw_uart_wait_T();

  digitalWrite(13, LOW);
  _sw_uart_wait_T();

  digitalWrite(13, HIGH);
  

  delay(2000);


}

void _sw_uart_wait_half_T() {
  for(int i = 0; i < 1093; i++)
    asm("NOP");
}

void _sw_uart_wait_T() {
  _sw_uart_wait_half_T();
  _sw_uart_wait_half_T();
}
