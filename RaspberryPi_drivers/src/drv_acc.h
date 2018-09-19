#define uint8_t	unsigned char

#define uint16_t unsigned short int

int read_reg(int address);

extern void init_acc();

extern int turn_acc_on();

extern void turn_acc_off();

extern bool is_acc_on();

extern void imu_self_test();

extern void drv_acc_measure(uint16_t *all_axis);
