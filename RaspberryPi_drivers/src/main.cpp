#include <iostream>
#include "drv_acc.h"
#include "socket_server.h"
#include <wiringPi.h>
#include <fstream>
#include <chrono>

#define RED_LED_OFF "python3 /home/pi/Documents/Git/PolesDetection/RaspberryPi_drivers/src/green_led_off.py"
#define RED_LED_ON  "python3 /home/pi/Documents/Git/PolesDetection/RaspberryPi_drivers/src/green_led_on.py"

std::ofstream file("/home/pi/Documents/Git/PolesDetection/RaspberryPi_drivers/bin/measurment.txt",std::fstream::out | std::fstream::app);

int main(void)
{	
	int16_t measure_data[3u];
	Accelerometer acc(1);
	std::chrono::duration<double> time;
	
	auto start = std::chrono::high_resolution_clock::now();
	auto stop = std::chrono::high_resolution_clock::now();
	
	std::cout << " X\t\tY\t\tZ\t\tTime[us]" << std::endl;
	file << " X\t\tY\t\tZ\t\tTime[us]" << std::endl;


	system(RED_LED_OFF);
	wait_for_tcp_conn();
	system(RED_LED_ON);

	while (1)
	{
		start = std::chrono::high_resolution_clock::now();
		acc.measure(measure_data);
		
		std::cout << measure_data[0u] << "\t\t";
		std::cout << measure_data[1u] << "\t\t";
		std::cout << measure_data[2u] << "\t\t";
		std::cout << time.count()  << "\n";
		
		file << measure_data[0u] << "\t\t";
		file << measure_data[1u] << "\t\t";
		file << measure_data[2u] << "\t\t";
		file << time.count()  << "\n";
	
		stop = std::chrono::high_resolution_clock::now();
		time += stop - start;
	}
	
	acc.turn_off();
	
	return 0;
}


