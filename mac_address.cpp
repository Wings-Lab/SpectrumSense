#include <stdio.h>
#include <stdlib.h>
#include <string>

#include <iostream>
// using namespace std;
std::string get_mac(){

    const int size = 256;
    
    char ip_address[size];
    int hw_type;
    int flags;
    char mac_address[size];
    char mask[size];
    char device[size];

    FILE* fp = fopen("/proc/net/arp", "r");
    if(fp == NULL)
    {
        perror("Error opening /proc/net/arp");
    }

    char line[size];
    fgets(line, size, fp);    // Skip the first line, which consists of column headers.
    while(fgets(line, size, fp))
    {
        sscanf(line, "%s 0x%x 0x%x %s %s %s\n",
               ip_address,
               &hw_type,
               &flags,
               mac_address,
               mask,
               device);

        // printf("IP = %s, MAC = %s", ip_address, mac_address);
    }
    fclose(fp);
    return mac_address;
}


int main(int argc, char** argv)
{
  std::string mac = get_mac();
  std::cout << mac;
}