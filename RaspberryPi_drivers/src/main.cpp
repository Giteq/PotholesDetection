#include <iostream>
#include "drv_acc.h"
#include "socket_server.h"
#include <wiringPi.h>
#include <fstream>
#include <unistd.h>

#define RED_LED_OFF "python3 /home/pi/Documents/Git/PolesDetection/RaspberryPi_drivers/src/green_led_off.py"
#define RED_LED_ON  "python3 /home/pi/Documents/Git/PolesDetection/RaspberryPi_drivers/src/green_led_on.py"

std::ofstream file("/home/pi/Documents/Git/PolesDetection/RaspberryPi_drivers/bin/measurment.txt",std::fstream::out | std::fstream::app);

int main(void)
{	
	int16_t measure[3u];
	Accelerometer acc;
	unsigned long long int time = 0;
	
	std::cout << " X\t\tY\t\tZ\t\tTime[us]\n\r";
	file << " X\t\tY\t\tZ\t\tTime[us]\n\r";

	while (1)
	{
		acc.measure(measure);
		std::cout << measure[0u] << "\t\t";
		std::cout << measure[1u] << "\t\t";
		std::cout << measure[2u] << "\t\t";
		std::cout << time << "\n";
		
		file << measure[0u] << "\t\t";
		file << measure[1u] << "\t\t";
		file << measure[2u] << "\t\t";
		file << time << "\n";
		usleep(1250u);
		time += 1250u;
	}
	
	acc.turn_off();
	
	return 0;
}

