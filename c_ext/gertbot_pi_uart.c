#include <unistd.h>   
#include <fcntl.h>    
#include <termios.h>  
#include <string.h>
#include <stdio.h>

int open_uart(int h)
{
  struct termios options;
  int handle = h;
  if (handle!=-1)
    return handle; // assume already opened
  handle = open("/dev/ttyAMA0", O_RDWR | O_NOCTTY | O_NDELAY);  //Open in non blocking read/write mode
  if (handle == -1)
  {
    fprintf(stderr,"Error - Unable to open UART. Ensure it is not in use by another application\n");
    fflush(stderr);
    return -1;
  }

  tcgetattr(handle, &options);
  cfsetospeed(&options,B57600);
  cfsetispeed(&options,B57600);
  options.c_cflag =  (options.c_cflag & ~CSIZE) | CS8; // 8 bits
  options.c_cflag |=  CLOCAL | CREAD;  // ignore mode status, enable rec.
  options.c_cflag &=  ~(PARENB | PARODD | CSTOPB); // No parity, 1 stop bit
 
  options.c_iflag = IGNBRK;
  options.c_iflag &= ~(IXON|IXOFF|IXANY);

  options.c_oflag = 0;
  options.c_lflag = 0;
  tcsetattr(handle, TCSANOW, &options); // set the options NOW
  return handle;
}

void close_uart(int handle)
{
  if (handle!=-1)
    close(handle);
}

int write_uart(int handle, unsigned char *data,int bytes)
{ 
  int length = bytes;
  #ifdef TEST
  printf("handle: %d\n", handle);
  printf("bytes: %d\ndata: ", length);
  for (int i=0; i<length; ++i)
    printf("%d ", (int) data[i]);
  printf("\n---\n");
  #endif
  int txed;
  int offset=0;
  while (length)
  {
    txed = write(handle, (unsigned char*)data+offset, length);
    if (txed==-1)
    { fprintf(stderr,"UART WRITE ERRROR!!\n");
      return 0;
    }
    length -= txed;
    offset += txed;
  }
  tcdrain(handle);
  return 1;
}

int  read_uart(int handle, unsigned char *data,int len)
{ 
  printf("calling read_uart\n");
  int rec,rep,tot;
  rep = len;  // use lenght as repeat 
  tot = 0;
  while (len>0 && rep)
  {
    rec = read(handle,(void *)data,len);
    if (rec<=0)   // if we got no data

    { usleep(5000); // Wait 5 milli seconds 
      rep--; // time out after a while 
    }
    else
    { tot += rec;
      len -= rec;
      data += rec;  // move pointer to after what we already have 
    } 
  } 
  return tot;
}
