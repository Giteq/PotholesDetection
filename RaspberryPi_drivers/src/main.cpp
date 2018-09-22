#include <iostream>
#include "drv_acc.h"
#include "socket_server.h"
#include <wiringPi.h>
#include <fstream>
#include <unistd.h>
#include <sys/time.h>

#define RED_LED_OFF "python3 /home/pi/Documents/Git/PolesDetection/RaspberryPi_drivers/src/green_led_off.py"
#define RED_LED_ON  "python3 /home/pi/Documents/Git/PolesDetection/RaspberryPi_drivers/src/green_led_on.py"

std::ofstream file("/home/pi/Documents/Git/PolesDetection/RaspberryPi_drivers/bin/measurment.txt",std::fstream::out | std::fstream::app);

static unsigned long calc_one_measure_time(Accelerometer acc);

static void delay_us(unsigned int us);

int main(void)
{	
	int16_t measure_data[3u];
	Accelerometer acc;
	unsigned long long int time = 0;
	unsigned long measure_delay = calc_one_measure_time(acc);
	
	std::cout << " X\t\tY\t\tZ\t\tTime[us]\n\r";
	file << " X\t\tY\t\tZ\t\tTime[us]\n\r";

	while (1)
	{
		acc.measure(measure_data);
		std::cout << measure_data[0u] << "\t\t";
		std::cout << measure_data[1u] << "\t\t";
		std::cout << measure_data[2u] << "\t\t";
		std::cout << time << "\n";
		
		file << measure_data[0u] << "\t\t";
		file << measure_data[1u] << "\t\t";
		file << measure_data[2u] << "\t\t";
		file << time << "\n";
	
		
		//delay_us(1250u - (measure_delay / 1000u));
		time += measure_delay;
	}
	
	acc.turn_off();
	
	return 0;
}

unsigned long calc_one_measure_time(Accelerometer acc)
{
	struct timespec time_now;
	unsigned long start;
	int16_t measure_data[3u];
	clock_gettime(CLOCK_REALTIME, & time_now);
	start = time_now.tv_nsec;
	acc.measure(measure_data);
	clock_gettime(CLOCK_REALTIME, & time_now);
	return time_now.tv_nsec - start;
}

void delay_us(unsigned int us)
{
	struct timespec time_now;
	unsigned long int start_nsec;
	clock_gettime(CLOCK_REALTIME, & time_now);
	start_nsec = time_now.tv_nsec;
	
	for (;;)
	{
		clock_gettime(CLOCK_REALTIME, &time_now);
		
		if (time_now.tv_nsec - start_nsec > us * 1000u)
		{
			break;
		}
	}
	
}

