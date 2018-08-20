#include <memory>
#include <condition_variable>

#include <kaa/Kaa.hpp>
#include <kaa/logging/Log.hpp>
#include <kaa/logging/LoggingUtils.hpp>
#include <kaa/notification/INotificationTopicListListener.hpp>
#include <kaa/common/exception/UnavailableTopicException.hpp>
#include <rtl-sdr.h>
#include "convenience/convenience.hpp"
#include <memory>
#include <string>
#include <cstdint>
#include <iostream>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <string.h>
#include <stdio.h>
#include <cstdlib>
#include <ncurses.h>
#include <kaa/log/strategies/RecordCountLogUploadStrategy.hpp>
#include <kaa/log/ILogStorageStatus.hpp>
#include <ctime>
/* timestamp example */
#include <stdio.h>      /* printf */
#include <time.h>       /* time_t, time (for timestamp in second) */
#include <sys/timeb.h>  /* ftime, timeb (for timestamp in millisecond) */
#include <sys/time.h>   /* gettimeofday, timeval (for timestamp in microsecond) */
#include <stdio.h>
#include <stdlib.h>
#include <string>

using namespace kaa;
#define DEFAULT_SAMPLE_RATE 2048000
static constexpr auto TOPIC_LIST_UPDATE_TIMEOUT = 3;
static bool switch_flag = false;
static int samplingPeriod = 1; //seconds
static std::string numberOfBins = "20";
static std::string numberOfSpectraToAvg = "32";
rtlsdr_dev_t *dev = NULL;
std::string cmd_for_power = "./rtl_power_fftw -q -b 2 -f 915.8e6 -e 2m  -g 1";


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
    return ip_address;
}


long long int get_timestamp()
{
  struct timeval timer_usec; 
  long int timestamp_usec; /* timestamp in microsecond */
  if (!gettimeofday(&timer_usec, NULL)) {
    timestamp_usec = (( long int) timer_usec.tv_sec) * 1000000ll + 
                        (long int) timer_usec.tv_usec;
  }
  else {
    timestamp_usec = -1;
  }
  
  return timestamp_usec;
}

static void set_up_device() 
{
    static rtlsdr_dev_t *dev = NULL;
    int dev_index = 0;
    int r;
    dev_index = verbose_device_search("0");
    r = rtlsdr_open(&dev, (uint32_t)dev_index);
    if (r < 0) 
    {
        printf("Failed to open device");
        exit (1);
    }
    verbose_set_sample_rate(dev, DEFAULT_SAMPLE_RATE);
    verbose_set_frequency(dev, 915800000);
    verbose_gain_set(dev, 1);
    verbose_ppm_set(dev, 0);
    verbose_reset_buffer(dev);
}


static void toggleFlag()
{        
    int error = 9999;
    switch_flag = !switch_flag;
    if (switch_flag){
        set_up_device();
    }else{
        error = rtlsdr_close(dev);
        std::cout << "Close device status: " << error << std::endl;
    }
}

static void modifySamplingPeriod(const KaaNotification &notification)
{
    std::cout << "New sampling period :" << notification.NewSamplingFrequency << std::endl;
    int num;
    const char *c;
    c = notification.NewSamplingFrequency.c_str();
    //std::cout << "New sampling period STRING:" << c << std::endl; 
    num = std::stoi(c);
    //std::cout << "New sampling period :" << num << std::endl;
    samplingPeriod = num;
}


static void modifyNumberOfBins(const KaaNotification &notification)
{
    std::cout << "New number of bins:" << notification.NewNumberOFBins << std::endl;
    numberOfBins = notification.NewNumberOFBins.c_str();
    std::string newCommand = "./rtl_power_fftw -n "+numberOfSpectraToAvg+" -q -b "+numberOfBins+" -f 916e6 -g 1";
    std::cout << "New command: " << newCommand << std::endl;
}

static void modifyNumberOfSpectraToAvg(const KaaNotification &notification)
{
    std::cout << "New number of spectra to avg:" << notification.NewNoAvgdSpectra << std::endl;
    numberOfSpectraToAvg = notification.NewNoAvgdSpectra.c_str();
    std::string newCommand = "./rtl_power_fftw -n "+numberOfSpectraToAvg+" -q -b "+numberOfBins+" -f 916e6 -g 1";
    std::cout << "New command: " << newCommand << std::endl;
}

static void processNotification(const KaaNotification &notification, const kaa_notification::power_iq_change_choice powiqChange)
{
    const char *samplefreq;
    const char *bins;
    const char *avgdspectra;
    
    samplefreq = notification.NewSamplingFrequency.c_str();
    bins = notification.NewNumberOFBins.c_str();
    avgdspectra = notification.NewNoAvgdSpectra.c_str();
    
    //const kaa_notification::PowIq_change powiqChange = notification.PowIQ_change;
    switch(powiqChange)
    {
        case kaa_notification::Y_change:
            toggleFlag();
            std::cout << "Changing Power IQ switch" << std::endl;
            break;
        case kaa_notification::N_change:
            break;
    }
    
    if(samplefreq[0] != '0')
    {
        std::cout << "Changing Sampling Frequency" << std::endl;
        modifySamplingPeriod(notification);
    }
    if(bins[0] != '0')
    {
        std::cout << "Changing number of bins" << std::endl;
        modifyNumberOfBins(notification);
    }
    if(avgdspectra[0] != '0')
    {
        std::cout << "Changing number of spectra to average" << std::endl;
        modifyNumberOfSpectraToAvg(notification);
    }
}

#define READ 0
#define WRITE 1

#define RAW_SIZE (4 * 1024) 
static  int exec_raw(unsigned char *array) 
{
    uint32_t out_block_size = RAW_SIZE;
    int n_read = RAW_SIZE;
    std::cout << dev; 
    int r = rtlsdr_read_sync(dev, array, out_block_size, &n_read);
    if (r < 0) 
    {
        printf("Error in reading");
        return (1);
    }
    return (0);
}

static void extractData(std::shared_ptr<IKaaClient> kaaClient)
{
    if (!switch_flag) 
    {
        char buffer[128];
        const char *cmd = cmd_for_power.c_str();
        std::shared_ptr<FILE> pipe(popen(cmd, "r"), pclose);
        if (!pipe) throw std::runtime_error("popen() failed!");
            while (!feof(pipe.get())) 
            {
                
                if (fgets(buffer, 128, pipe.get()) != nullptr) 
                {
                    std::stringstream ss;
                    ss << buffer;
                    kaa::KaaUserLogRecord logRecord;
                    ss >> logRecord.frequency;
                    ss >> logRecord.power;
                    logRecord.nodenumber = get_mac();
                    logRecord.timestamp = get_timestamp();
                    auto recordDeliveryCallback = kaaClient->addLogRecord(logRecord);
                    // while(1)
                    // {
                    //     try {
                    //         auto recordInfo = recordDeliveryCallback.get();
                    //         auto bucketInfo = recordInfo.getBucketInfo();
                    //         std::cout << "Received log record delivery info. Bucket Id [" <<  bucketInfo.getBucketId() << "]. "
                    //                   << "Record delivery time [" << recordInfo.getRecordDeliveryTimeMs() << " ms]." << std::endl;
                    //         break;          
                    //     } catch (std::exception& e) {
                    //         std::cout << "Exception was caught while waiting for callback result: " << e.what() << std::endl;
                    //     }

                    // }

                    //std::cout << "Sampled power and frequency: " << logRecord.power << " " << logRecord.frequency << std::endl;
                }
                

            }
        /*kaa::KaaUserLogRecord logRecord;
    //srand(200);
        logRecord.frequency = (rand() % 20) + 8;
    logRecord.power = (rand() % 20) + 8;
        kaaClient->addLogRecord(logRecord);*/
    }
    else 
    {
        unsigned char *array = (unsigned char *)malloc(RAW_SIZE);
        exec_raw(array);    
        std::vector<unsigned char> vec(array, array + RAW_SIZE);
        kaa::KaaUserLogRecord logRecord;
        logRecord.frequency = logRecord.power = 0;
        logRecord.iq = vec;
        logRecord.nodenumber = get_mac();
        logRecord.timestamp = get_timestamp();
        kaaClient->addLogRecord(logRecord);
        std::cout << "IQ data entered: " << std::endl;
        /*kaa::KaaUserLogRecord logRecord;
    //srand(50);
        logRecord.frequency = (rand() % 20) + 8;
        logRecord.power = (rand()% 20) + 8;
        kaaClient->addLogRecord(logRecord);*/
    }
}

class NotificationListener : public INotificationListener 
{
public:
    NotificationListener(std::shared_ptr<IKaaClient> kaaClient):
        kaaClient(kaaClient)
    {}

    void onNotification(const int64_t topicId, const KaaNotification &notification) override
    {
        auto topics = kaaClient->getTopics();
        const auto &topic = std::find_if(topics.begin(), topics.end(),
                [topicId](const Topic &t) { return t.id == topicId; });
        std::cout << (boost::format("Notification for topic id '%1%' and name '%2%' received") % topicId % topic->name) << std::endl;
        processNotification(notification, notification.power_iq_change);
    //std::cout << "Calling toggle flag method...." << std::endl;
    //processNotification(notification);
    
    }

private:
    std::shared_ptr<IKaaClient> kaaClient;
};


int main()
{
    auto kaaClient = Kaa::newClient();
    int counter = 0;
   
   //set_up_device();
    kaaClient->setLogUploadStrategy(std::make_shared<kaa::RecordCountLogUploadStrategy>(100, kaaClient->getKaaClientContext()));    
    NotificationListener notificationListener(kaaClient);
    kaaClient->addNotificationListener(notificationListener);
    std::cin.clear();
    kaaClient->start();

    std::cout << "Notification demo started" << std::endl;

    const auto &topics = kaaClient->getTopics();

    for(const auto &topic : topics)
    {
        std::cout << (boost::format("Topic ID-> %1%, Topic name-> %2%") % topic.id % topic.name) << std::endl;
    }
    switch_flag = false;
    {
        counter++;
        extractData(kaaClient);
    
        //std::cout << counter << "--->In loop with flag : " << switch_flag << std::endl;
        std::this_thread::sleep_for (std::chrono::seconds(samplingPeriod));
    }
    
    
    kaaClient->stop();

    return EXIT_SUCCESS;
}
