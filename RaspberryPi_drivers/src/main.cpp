#include <iostream>
#include "drv_acc.h"
#include "socket_server.h"
#include <wiringPi.h>
#include <fstream>
#include <chrono>
#include <string>

#define RED_LED_OFF "python3 /home/pi/Documents/Git/PolesDetection/RaspberryPi_drivers/src/green_led_off.py"
#define RED_LED_ON  "python3 /home/pi/Documents/Git/PolesDetection/RaspberryPi_drivers/src/green_led_on.py"

std::ofstream acc_file;;

std::ofstream gyro_file;

std::string measunre_no_path = "/home/pi/Desktop/measurments/last_measure.txt";

std::ifstream measure_number(measunre_no_path);

std::ofstream o_measure_number;


int main(void)
{	
	int meas_num;
	measure_number >> meas_num;
	
	std::string acc_output_name = "/home/pi/Desktop/measurments/acc/";
	std::string gyro_output_name = "/home/pi/Desktop/measurments/gyro/";
	acc_output_name += std::to_string(meas_num);
	acc_output_name += ".txt";
	gyro_output_name += std::to_string(meas_num);
	gyro_output_name += ".txt";
	
	acc_file.open(acc_output_name, std::fstream::out | std::fstream::app);
	gyro_file.open(gyro_output_name, std::fstream::out | std::fstream::app);
	
	measure_number.close();
	o_measure_number.open(measunre_no_path, std::ofstream::out | std::ofstream::trunc);
	o_measure_number << (int)(meas_num) + 1;
	
	o_measure_number.close();
	
	int16_t measure_data[3u];
	Accelerometer acc(2);
	std::chrono::duration<double> time;
	
	Accelerometer gyro(3);
	
	auto start = std::chrono::high_resolution_clock::now();
	auto stop = std::chrono::high_resolution_clock::now();
	
	std::cout << " X\t\tY\t\tZ\t\tTime[us]" << std::endl;
	acc_file << " X\t\tY\t\tZ\t\tTime[us]" << std::endl;
	gyro_file << " X\t\tY\t\tZ\t\tTime[us]" << std::endl;


	//system(RED_LED_OFF);
	wait_for_tcp_conn();
	//system(RED_LED_ON);
	
	//std::cout << "Wartosc " << gyro.read_reg(0x11) << std::endl;
	
	while (1)
	{
		start = std::chrono::high_resolution_clock::now();
		acc.measure(measure_data);
		
		std::cout << measure_data[0u] << "\t\t";
		std::cout << measure_data[1u] << "\t\t";
		std::cout << measure_data[2u] << "\t\t";
		std::cout << time.count()  << "\n";
		
		acc_file << measure_data[0u] << "\t\t";
		acc_file << measure_data[1u] << "\t\t";
		acc_file << measure_data[2u] << "\t\t";
		acc_file << time.count()  << "\n";
	
		gyro.measure(measure_data);
		
		gyro_file << measure_data[0u] << "\t\t";
		gyro_file << measure_data[1u] << "\t\t";
		gyro_file << measure_data[2u] << "\t\t";
		gyro_file << time.count()  << "\n";
	
		stop = std::chrono::high_resolution_clock::now();
		time += stop - start;
	}
	
	acc.turn_off();
	gyro_file.close();
	acc_file.close();
	return 0;
}


