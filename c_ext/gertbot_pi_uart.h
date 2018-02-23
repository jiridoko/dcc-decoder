//
//
// Pi UART interface header file 
//
//


//
// Open UART in correct mode for Gertbot:
// 8 bits, 1 start, 1 stop, no parity
// No HW flow control non blocking
// 
// if low use 57600 baud else use 115K2 baud
int open_uart(int handle);

// close uart
// No return status
// (if this fails we are in big trouble anway)
void close_uart(int handle);

//
// transmit data to uart 
//
// return 0 on failure
// return 1 on success
//
int write_uart(int handle, unsigned char *data,int bytes);

//
// Try to read at least 'len' characters from uart (len<=32) 
// Beware: this routine can return more then asked for, up to 64 bytes
// Thus data should point to area of 64 unsigned chars!!!!
//
// return the actual number of bytes read 
// 
int  read_uart(int handle, unsigned char *data,int len);
