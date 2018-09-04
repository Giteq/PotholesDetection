#include <iostream>
#include "drv_acc.h"
#include "socket_server.h"
#include "gpio.h"
#include <wiringPi.h>

#define RED_LED_OFF "python3 /home/pi/Documents/Git/PolesDetection/RaspberryPi_drivers/src/green_led_off.py"
#define RED_LED_ON  "python3 /home/pi/Documents/Git/PolesDetection/RaspberryPi_drivers/src/green_led_on.py"

int main(void)
{
	system(RED_LED_OFF);
	wait_for_tcp_conn();
	system(RED_LED_ON);
	//std::cout << "Ret val" <<  turn_acc_on() <<"\n";
	//imu_self_test();
	
	return 0;
}

