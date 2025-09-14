const int red1 = 23;
const int red2 = 22;
const int red3 = 21;
const int red4 = 19;

const int yellow1 = 18;
const int yellow2 = 5;
const int yellow3 = 17;
const int yellow4 = 16;

const int green1 = 26;
const int green2 = 25;
const int green3 = 32;
const int green4 = 33;

void setup() {
    pinMode(red1, OUTPUT); pinMode(yellow1, OUTPUT); pinMode(green1, OUTPUT);
    pinMode(red2, OUTPUT); pinMode(yellow2, OUTPUT); pinMode(green2, OUTPUT);
    pinMode(red3, OUTPUT); pinMode(yellow3, OUTPUT); pinMode(green3, OUTPUT);
    pinMode(red4, OUTPUT); pinMode(yellow4, OUTPUT); pinMode(green4, OUTPUT);
}

void loop() {

  // 1st GREEN Signal
digitalWrite(red1,LOW);digitalWrite(yellow1,LOW);digitalWrite(green1,HIGH);
digitalWrite(red2,HIGH);digitalWrite(yellow2,LOW);digitalWrite(green2,LOW);
digitalWrite(red3,HIGH);digitalWrite(yellow3,LOW);digitalWrite(green3,LOW);
digitalWrite(red4,HIGH);digitalWrite(yellow4,LOW);digitalWrite(green4,LOW);
delay(5000);

  // Yellow Light
digitalWrite(red1,LOW);digitalWrite(yellow1,HIGH);digitalWrite(green1,LOW);
digitalWrite(red2,LOW);digitalWrite(yellow2,HIGH);digitalWrite(green2,LOW);
digitalWrite(red3,HIGH);digitalWrite(yellow3,LOW);digitalWrite(green3,LOW);
digitalWrite(red4,HIGH);digitalWrite(yellow4,LOW);digitalWrite(green4,LOW);
delay(1000);

  // 2nd GREEN Signal
digitalWrite(red1,HIGH);digitalWrite(yellow1,LOW);digitalWrite(green1,LOW);
digitalWrite(red2,LOW);digitalWrite(yellow2,LOW);digitalWrite(green2,HIGH);
digitalWrite(red3,HIGH);digitalWrite(yellow3,LOW);digitalWrite(green3,LOW);
digitalWrite(red4,HIGH);digitalWrite(yellow4,LOW);digitalWrite(green4,LOW);
delay(5000);

  // Yellow Light
digitalWrite(red1,HIGH);digitalWrite(yellow1,LOW);digitalWrite(green1,LOW);
digitalWrite(red2,LOW);digitalWrite(yellow2,HIGH);digitalWrite(green2,LOW);
digitalWrite(red3,LOW);digitalWrite(yellow3,HIGH);digitalWrite(green3,LOW);
digitalWrite(red4,HIGH);digitalWrite(yellow4,LOW);digitalWrite(green4,LOW);
delay(1000);

  // 3rd GREEN Signal
digitalWrite(red1,HIGH);digitalWrite(yellow1,LOW);digitalWrite(green1,LOW);
digitalWrite(red2,HIGH);digitalWrite(yellow2,LOW);digitalWrite(green2,LOW);
digitalWrite(red3,LOW);digitalWrite(yellow3,LOW);digitalWrite(green3,HIGH);
digitalWrite(red4,HIGH);digitalWrite(yellow4,LOW);digitalWrite(green4,LOW);
delay(5000);

  // Yellow Light
digitalWrite(red1,HIGH);digitalWrite(yellow1,LOW);digitalWrite(green1,LOW);
digitalWrite(red2,HIGH);digitalWrite(yellow2,LOW);digitalWrite(green2,LOW);
digitalWrite(red3,LOW);digitalWrite(yellow3,HIGH);digitalWrite(green3,LOW);
digitalWrite(red4,LOW);digitalWrite(yellow4,HIGH);digitalWrite(green4,LOW);
delay(1000);

  // 4th GREEN Signal
digitalWrite(red1,HIGH);digitalWrite(yellow1,LOW);digitalWrite(green1,LOW);
digitalWrite(red2,HIGH);digitalWrite(yellow2,LOW);digitalWrite(green2,LOW);
digitalWrite(red3,HIGH);digitalWrite(yellow3,LOW);digitalWrite(green3,LOW);
digitalWrite(red4,LOW);digitalWrite(yellow4,LOW);digitalWrite(green4,HIGH);
delay(5000);

  // Yellow Light
digitalWrite(red1,LOW);digitalWrite(yellow1,HIGH);digitalWrite(green1,LOW);
digitalWrite(red2,HIGH);digitalWrite(yellow2,LOW);digitalWrite(green2,LOW);
digitalWrite(red3,HIGH);digitalWrite(yellow3,LOW);digitalWrite(green3,LOW);
digitalWrite(red4,LOW);digitalWrite(yellow4,HIGH);digitalWrite(green4,LOW);
delay(1000);
} 
