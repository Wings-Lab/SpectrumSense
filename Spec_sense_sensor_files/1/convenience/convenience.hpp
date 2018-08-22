/*
 * Copyright (C) 2014 by Kyle Keen <keenerd@gmail.com>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

/* a collection of user friendly tools */

/*!
 * Convert standard suffixes (k, M, G) to double
 *
 * \param s a string to be parsed
 * \return double
 */

double atofs(char *s);

/*!
 * Convert time suffixes (s, m, h) to double
 *
 * \param s a string to be parsed
 * \return seconds as double
 */

double atoft(char *s);

/*!
 * Convert percent suffixe (%) to double
 *
 * \param s a string to be parsed
 * \return double
 */

double atofp(char *s);

/*!
 * Find nearest supported gain
 *
 * \param dev the device handle given by rtlsdr_open()
 * \param target_gain in tenths of a dB
 * \return 0 on success
 */

int nearest_gain(rtlsdr_dev_t *dev, int target_gain);

/*!
 * Set device frequency and report status on stderr
 *
 * \param dev the device handle given by rtlsdr_open()
 * \param frequency in Hz
 * \return 0 on success
 */

int verbose_set_frequency(rtlsdr_dev_t *dev, uint32_t frequency);

/*!
 * Set device sample rate and report status on stderr
 *
 * \param dev the device handle given by rtlsdr_open()
 * \param samp_rate in samples/second
 * \return 0 on success
 */

int verbose_set_sample_rate(rtlsdr_dev_t *dev, uint32_t samp_rate);

/*!
 * Enable or disable the direct sampling mode and report status on stderr
 *
 * \param dev the device handle given by rtlsdr_open()
 * \param on 0 means disabled, 1 I-ADC input enabled, 2 Q-ADC input enabled
 * \return 0 on success
 */

int verbose_direct_sampling(rtlsdr_dev_t *dev, int on);

/*!
 * Enable offset tuning and report status on stderr
 *
 * \param dev the device handle given by rtlsdr_open()
 * \return 0 on success
 */

int verbose_offset_tuning(rtlsdr_dev_t *dev);

/*!
 * Enable auto gain and report status on stderr
 *
 * \param dev the device handle given by rtlsdr_open()
 * \return 0 on success
 */

int verbose_auto_gain(rtlsdr_dev_t *dev);

/*!
 * Set tuner gain and report status on stderr
 *
 * \param dev the device handle given by rtlsdr_open()
 * \param gain in tenths of a dB
 * \return 0 on success
 */

int verbose_gain_set(rtlsdr_dev_t *dev, int gain);

/*!
 * Set the frequency correction value for the device and report status on stderr.
 *
 * \param dev the device handle given by rtlsdr_open()
 * \param ppm_error correction value in parts per million (ppm)
 * \return 0 on success
 */

int verbose_ppm_set(rtlsdr_dev_t *dev, int ppm_error);

/*!
 * Reset buffer
 *
 * \param dev the device handle given by rtlsdr_open()
 * \return 0 on success
 */

int verbose_reset_buffer(rtlsdr_dev_t *dev);

/*!
 * Find the closest matching device.
 *
 * \param s a string to be parsed
 * \return dev_index int, -1 on error
 */

int verbose_device_search(char *s);

double atofs(char *s)
/* standard suffixes */
{
        char last;
        int len;
        double suff = 1.0;
        len = strlen(s);
        last = s[len-1];
        s[len-1] = '\0';
        switch (last) {
                case 'g':
                case 'G':
                        suff *= 1e3;
                case 'm':
                case 'M':
                        suff *= 1e3;
                case 'k':
                case 'K':
                        suff *= 1e3;
                        suff *= atof(s);
                        s[len-1] = last;
                        return suff;
        }
        s[len-1] = last;
        return atof(s);
}

double atoft(char *s)
/* time suffixes, returns seconds */
{
        char last;
        int len;
        double suff = 1.0;
        len = strlen(s);
        last = s[len-1];
        s[len-1] = '\0';
        switch (last) {
                case 'h':
                case 'H':
                        suff *= 60;
                case 'm':
                case 'M':
                        suff *= 60;
                case 's':
                case 'S':
                        suff *= atof(s);
                        s[len-1] = last;
                        return suff;
        }
        s[len-1] = last;
        return atof(s);
}

double atofp(char *s)
/* percent suffixes */
{
        char last;
        int len;
        double suff = 1.0;
        len = strlen(s);
        last = s[len-1];
        s[len-1] = '\0';
        switch (last) {
                case '%':
                        suff *= 0.01;
                        suff *= atof(s);
                        s[len-1] = last;
                        return suff;
        }
        s[len-1] = last;
        return atof(s);
}


int nearest_gain(rtlsdr_dev_t *dev, int target_gain)
{
        int i, r, err1, err2, count, nearest;
        int* gains;
        r = rtlsdr_set_tuner_gain_mode(dev, 1);
        if (r < 0) {
                fprintf(stderr, "WARNING: Failed to enable manual gain.\n");
                return r;
        }
        count = rtlsdr_get_tuner_gains(dev, NULL);
        if (count <= 0) {
                return 0;
        }
        gains = (int *)malloc(sizeof(int) * count);
        count = rtlsdr_get_tuner_gains(dev, gains);
        nearest = gains[0];
        for (i=0; i<count; i++) {
                err1 = abs(target_gain - nearest);
                err2 = abs(target_gain - gains[i]);
                if (err2 < err1) {
                        nearest = gains[i];
                }
        }
        free(gains);
        return nearest;
}

int verbose_set_frequency(rtlsdr_dev_t *dev, uint32_t frequency)
{
        int r;
        r = rtlsdr_set_center_freq(dev, frequency);
        if (r < 0) {
                fprintf(stderr, "WARNING: Failed to set center freq.\n");
        } else {
                fprintf(stderr, "Tuned to %u Hz.\n", frequency);
        }
        return r;
}

int verbose_set_sample_rate(rtlsdr_dev_t *dev, uint32_t samp_rate)
{
        int r;
        r = rtlsdr_set_sample_rate(dev, samp_rate);
        if (r < 0) {
                fprintf(stderr, "WARNING: Failed to set sample rate.\n");
        } else {
                fprintf(stderr, "Sampling at %u S/s.\n", samp_rate);
        }
        return r;
}

int verbose_direct_sampling(rtlsdr_dev_t *dev, int on)
{
        int r;
        r = rtlsdr_set_direct_sampling(dev, on);
        if (r != 0) {
                fprintf(stderr, "WARNING: Failed to set direct sampling mode.\n");
                return r;
        }
        if (on == 0) {
                fprintf(stderr, "Direct sampling mode disabled.\n");}
        if (on == 1) {
                fprintf(stderr, "Enabled direct sampling mode, input 1/I.\n");}
        if (on == 2) {
                fprintf(stderr, "Enabled direct sampling mode, input 2/Q.\n");}
        return r;
}

int verbose_offset_tuning(rtlsdr_dev_t *dev)
{
        int r;
        r = rtlsdr_set_offset_tuning(dev, 1);
        if (r != 0) {
                fprintf(stderr, "WARNING: Failed to set offset tuning.\n");
        } else {
                fprintf(stderr, "Offset tuning mode enabled.\n");
        }
        return r;
}

int verbose_auto_gain(rtlsdr_dev_t *dev)
{
        int r;
        r = rtlsdr_set_tuner_gain_mode(dev, 0);
        if (r != 0) {
                fprintf(stderr, "WARNING: Failed to set tuner gain.\n");
        } else {
                fprintf(stderr, "Tuner gain set to automatic.\n");
        }
        return r;
}

int verbose_gain_set(rtlsdr_dev_t *dev, int gain)
{
        int r;
        r = rtlsdr_set_tuner_gain_mode(dev, 1);
        if (r < 0) {
                fprintf(stderr, "WARNING: Failed to enable manual gain.\n");
                return r;
        }
        r = rtlsdr_set_tuner_gain(dev, gain);
        if (r != 0) {
                fprintf(stderr, "WARNING: Failed to set tuner gain.\n");
        } else {
                fprintf(stderr, "Tuner gain set to %0.2f dB.\n", gain/10.0);
        }
        return r;
}

int verbose_ppm_set(rtlsdr_dev_t *dev, int ppm_error)
{
        int r;
        if (ppm_error == 0) {
                return 0;}
        r = rtlsdr_set_freq_correction(dev, ppm_error);
        if (r < 0) {
                fprintf(stderr, "WARNING: Failed to set ppm error.\n");
        } else {
                fprintf(stderr, "Tuner error set to %i ppm.\n", ppm_error);
        }
        return r;
}

int verbose_reset_buffer(rtlsdr_dev_t *dev)
{
        int r;
        r = rtlsdr_reset_buffer(dev);
        if (r < 0) {
                fprintf(stderr, "WARNING: Failed to reset buffers.\n");}
        return r;
}

int verbose_device_search(char *s)
{
        int i, device_count, device, offset;
        char *s2;
        char vendor[256], product[256], serial[256];
        device_count = rtlsdr_get_device_count();
        if (!device_count) {
                fprintf(stderr, "No supported devices found.\n");
                return -1;
        }
        fprintf(stderr, "Found %d device(s):\n", device_count);
        for (i = 0; i < device_count; i++) {
                rtlsdr_get_device_usb_strings(i, vendor, product, serial);
                fprintf(stderr, "  %d:  %s, %s, SN: %s\n", i, vendor, product, serial);
        }
        fprintf(stderr, "\n");
        /* does string look like raw id number */
        device = (int)strtol(s, &s2, 0);
        if (s2[0] == '\0' && device >= 0 && device < device_count) {
                fprintf(stderr, "Using device %d: %s\n",
                        device, rtlsdr_get_device_name((uint32_t)device));
                return device;
        }
        /* does string exact match a serial */
        for (i = 0; i < device_count; i++) {
                rtlsdr_get_device_usb_strings(i, vendor, product, serial);
                if (strcmp(s, serial) != 0) {
                        continue;}
                device = i;
                fprintf(stderr, "Using device %d: %s\n",
                        device, rtlsdr_get_device_name((uint32_t)device));
                return device;
        }

 /* does string suffix match a serial */
        for (i = 0; i < device_count; i++) {
                rtlsdr_get_device_usb_strings(i, vendor, product, serial);
                offset = strlen(serial) - strlen(s);
                if (offset < 0) {
                        continue;}
                if (strncmp(s, serial+offset, strlen(s)) != 0) {
                        continue;}
                device = i;
                fprintf(stderr, "Using device %d: %s\n",
                        device, rtlsdr_get_device_name((uint32_t)device));
                return device;
        }
        fprintf(stderr, "No matching devices found.\n");
        return -1;
}


