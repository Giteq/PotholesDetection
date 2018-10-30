#include <iostream>
#include <errno.h>
#include <wiringPiI2C.h>
#include <time.h>
#include <unistd.h>
#include "drv_acc.h"

/* Unique device identificator. */
#define ACC_IDENTIFICATOR 0xD7u

/* Default L3DG20H acc is chosed. */
#define L3GD20H_I2C_ADDR	0x6B



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
		this->write_reg(CTRL5, CTRL5_DEFAULT);
		this->write_reg(FIFO_CTRL, FIFO_CONTROL_DEFAULT);
	
		this->turn_on();
	}
	else
	{
		this->i2c_address = L3GD20H_I2C_ADDR;
		this->fd = wiringPiI2CSetup(this->i2c_address);
		this->write_reg(FIFO_CTRL5, FIFO_CTRL5_DEFAULT);
		this->write_reg(CTRL1_XL, CTRL1_XL_DEFAULT);
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
