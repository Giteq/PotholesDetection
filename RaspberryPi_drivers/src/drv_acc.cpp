#include <iostream>
#include <errno.h>
#include <wiringPiI2C.h>
#include <time.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include "drv_acc.h"

/* Unique device identificator. */
#define ACC_IDENTIFICATOR 0xD7u

/* Default L3DG20H acc is chosed. */
#define L3GD20H_I2C_ADDR	0x1D

#define GYRO_ADDR			0x6B

Accelerometer::Accelerometer()
{
	this->i2c_address = L3GD20H_I2C_ADDR;
	this->fd = wiringPiI2CSetup(this->i2c_address);
	this->write_reg(CTRL1, CTRL1_DEFAULT);
	this->write_reg(CTRL5, CTRL5_DEFAULT);
	this->write_reg(FIFO_CTRL, FIFO_CONTROL_DEFAULT);
	
	this->turn_on();
}

Accelerometer::Accelerometer(int acc_type)
{
	if (acc_type == 0)
	{
		this->i2c_address = L3GD20H_I2C_ADDR;
		this->fd = wiringPiI2CSetup(this->i2c_address);
		this->write_reg(CTRL1, CTRL1_DEFAULT);
		this->write_reg(CTRL0, CTRL0_DEFAULT);
		
		//this->write_reg(CTRL5, CTRL5_DEFAULT);
		//this->write_reg(FIFO_CTRL, FIFO_CONTROL_DEFAULT);
	
		//this->turn_on();
	}
	else
	{
		this->i2c_address = GYRO_ADDR;
		this->fd = wiringPiI2CSetup(this->i2c_address);
		this->write_reg(FIFO_CTRL5, FIFO_CTRL5_DEFAULT);
		this->write_reg(CTRL1_XL, CTRL1_XL_DEFAULT);
		this->write_reg(CTRL1, CTRL1_GYRO_DEFAULT);
		this->write_reg(CTRL0, CTRL0_DEFAULT);
		this->write_reg(CTRL5, CTRL5_DEFAULT);
		this->write_reg(FIFO_CTRL, FIFO_CONTROL_DEFAULT);
		this->turn_on();
		
	}

}

Accelerometer::Accelerometer(uint8_t i2c_address)
{
	this->i2c_address = i2c_address;
	this->fd = wiringPiI2CSetup(this->i2c_address);
	this->write_reg(CTRL1, CTRL1_DEFAULT);
	this->write_reg(CTRL5, CTRL5_DEFAULT);
	this->write_reg(FIFO_CTRL, FIFO_CONTROL_DEFAULT);
	
	this->turn_on();
}

void Accelerometer::measure(int16_t *all_axis)
{
	unsigned int x, y, z;
	x = (int8_t)this->read_reg(OUT_X_L);
	x |= ((int16_t)this->read_reg(OUT_X_H) << 8u);
	all_axis[0u] = x;
	y = (int8_t)this->read_reg(OUT_Y_L);
	y |= ((int16_t)this->read_reg(OUT_Y_H) << 8u);
	all_axis[1u] = y;
	z = (int8_t)this->read_reg(OUT_Z_L);
	z |= ((int16_t)this->read_reg(OUT_Z_H) << 8u);
	all_axis[2u] = z;
	
}

uint8_t Accelerometer::who_am_i(void)
{
	uint8_t ret_val = 0;
	ret_val =  this->read_reg(WHO_AM_I);
	return ret_val;
}

int16_t find_minimum(int16_t buffer[5][3], int axis)
{
	int16_t minimum = buffer[0][axis];
	
	for (int i=0; i<5; i++)
	{
		if (minimum > buffer[i][axis])
		{
			minimum = buffer[i][axis];
		}
	}
	return minimum;
}

int16_t find_maximum(int16_t buffer[5][3], int axis)
{
	int16_t maximum = buffer[0][axis];
	
	for (int i=0; i<5; i++)
	{
		if (maximum < buffer[i][axis])
		{
			maximum = buffer[i][axis];
		}
	}
	return maximum;
}

int16_t Accelerometer::self_test(void)
{
	
	int16_t out_nost[5u][3u];
	int16_t out_st[5u][3u];
	int16_t ret_val = 1;
		
	this->write_reg(CTRL1_XL, 0x30u);
	this->write_reg(CTRL2_G, 0x00u);
	this->write_reg(CTRL3_C, 0x44u);
	this->write_reg(CTRL4_C, 0x00u);
	this->write_reg(CTRL5_C, 0x00u);
	this->write_reg(CTRL6_G, 0x00u);
	this->write_reg(CTRL7_G, 0x00u);
	this->write_reg(CTRL8_XL, 0x00u);
	this->write_reg(CTRL9_XL, 0x38u);
	this->write_reg(CTRL10_C, 0x00u);
	
	sleep(1);
	
	int16_t status_reg = this->read_reg(STATUS_REG);
	
	/* Wait until data are available. */
	while ((status_reg & 0x01u) != 1)
	{
		status_reg = this->read_reg(STATUS_REG);
	}
	
	/* Clearing flag, data discared. */
	this->measure(out_nost[0u]);
	
	for (int i=0; i<5; i++)
	{
		this->measure(out_nost[i]);
	}
	int16_t out_nost_avrg[3u] = {0u};
	for (int j=0; j<3; j++)
	{
		for (int i=0; i<5; i++)
		{	
			out_nost_avrg[j] += out_nost[i][j];
		}
		out_nost_avrg[j] /= 5;
	}
	
	/* Enable ACC test. */	
	this->write_reg(CTRL5_C, 0x01u);
	
		/* Wait until data are available. */
	while ((status_reg & 0x01u) != 1)
	{
		status_reg = this->read_reg(STATUS_REG);
	}
	
	/* Clearing flag, data discared. */
	this->measure(out_st[0u]);
	
		for (int i=0; i<5; i++)
	{
		this->measure(out_nost[i]);
	}
	int16_t out_st_avrg[3u] = {0u};
	for (int j=0; j<3; j++)
	{
		for (int i=0; i<5; i++)
		{	
			out_st_avrg[j] += out_st[i][j];
		}
		out_st_avrg[j] /= 5;
	}
	int min, max;
	
	for (int i=0; i<3; i++)
	{
		min = find_minimum(out_st, i);
		max = find_maximum(out_st, i);
		if ( min > out_st_avrg[i] - out_nost_avrg[i])
		{
			ret_val = 0;
		}
		else if (max < out_st_avrg[i] - out_nost_avrg[i])
		{
			ret_val = 0;
		}
		if (ret_val == 0)
		{
			std::cout << "Blad na osi" <<i << std::endl;
		}
	}
	
	
	for (int i = 0; i<5; i++)
	{
		std::cout << "Nost = ";
		std::cout << "X = " << out_nost[i][0];
		std::cout << "\tY = "  << out_nost[i][1];
		std::cout << "\tZ = "  << out_nost[i][2] << std::endl;
	}
	for (int i=0; i<5; i++)
	{
		std::cout << "ST = ";
		std::cout << "X = "  << out_st[i][0];
		std::cout << "\tY = "  << out_st[i][1];
		std::cout << "\tZ = "  << out_st[i][2] << std::endl;
	}
	
	std::cout << "Min = " << min << "  Max = " << max << std::endl;
	
	this->write_reg(CTRL1_XL, 0x0);
	this->write_reg(CTRL5_C, 0x0);
	
	return ret_val;
}

int Accelerometer::write_reg(uint8_t address, uint8_t value)
{
	int ret_val;
	ret_val = wiringPiI2CWriteReg8(this->fd, address, value);
	
	return ret_val;
}

int Accelerometer::read_reg(int address)
{
	int ret_val;
	ret_val = wiringPiI2CReadReg8(this->fd, address);
	
	
	return ret_val;
}

int Accelerometer::turn_on()
{
	int ret_val;
	
	int actual_value = this->read_reg(CTRL1);
	
	/* Set 4 bit (Power mode). */
	actual_value |= 8;
	
	ret_val = this->write_reg(CTRL1, actual_value);
	
	return ret_val;
	
}

void Accelerometer::turn_off()
{
	int actual_value = this->read_reg(CTRL1);
	
	/* Clear 4 bit (Power mode). */
	actual_value &= 0xF7;
	
	this->write_reg(CTRL1, actual_value);
	
}

bool Accelerometer::is_on()
{
	bool ret_val = true;
	
	uint8_t ctrl1 = (uint8_t) this->read_reg(CTRL1);
	
	/* Ceck if 4 bit (Power mode) is set. */
	if ( (ctrl1 | 0xF7) != 255)
	{
		/* If isn't return false. */
		ret_val = false;
	}
	
	return ret_val;
}	
