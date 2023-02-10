Diff
~~~~

.. code-block:: diff

    @@ -1,4 +1,4 @@
    -static void setHeaderComment(wavHeader_t *wavHeader, uint32_t currentTime, int8_t timezoneHours, int8_t timezoneMinutes, uint8_t *serialNumber, uint32_t gain, AM_extendedBatteryState_t extendedBatteryState, int32_t temperature, bool supplyVoltageLow, bool switchPositionChanged, uint32_t amplitudeThreshold, AM_filterType_t filterType, uint32_t lowerFilterFreq, uint32_t higherFilterFreq) {
    +static void setHeaderComment(wavHeader_t *wavHeader, uint32_t currentTime, int8_t timezoneHours, int8_t timezoneMinutes, uint8_t *serialNumber, uint32_t gain, AM_extendedBatteryState_t extendedBatteryState, int32_t temperature, bool switchPositionChanged, bool supplyVoltageLow, bool fileSizeLimited, uint32_t amplitudeThreshold, AM_filterType_t filterType, uint32_t lowerFilterFreq, uint32_t higherFilterFreq) {
     
         time_t rawtime = currentTime + timezoneHours * SECONDS_IN_HOUR + timezoneMinutes * SECONDS_IN_MINUTE;
     
    @@ -82,17 +82,21 @@
     
         }
     
    -    if (supplyVoltageLow || switchPositionChanged) {
    +    if (supplyVoltageLow || switchPositionChanged || fileSizeLimited) {
     
             comment += sprintf(comment, " Recording cancelled before completion due to ");
     
    -        if (supplyVoltageLow) {
    +        if (switchPositionChanged) {
    +
    +            comment += sprintf(comment, "change of switch position.");
    +
    +        } else if (supplyVoltageLow) {
     
                 comment += sprintf(comment, "low voltage.");
     
    -        } else if (switchPositionChanged) {
    +        } else if (fileSizeLimited) {
     
    -            comment += sprintf(comment, "change of switch position.");
    +            comment += sprintf(comment, "file size limit.");
     
             }
     

Code
~~~~

.. code-block:: C

    static void setHeaderComment(wavHeader_t *wavHeader, uint32_t currentTime, int8_t timezoneHours, int8_t timezoneMinutes, uint8_t *serialNumber, uint32_t gain, AM_extendedBatteryState_t extendedBatteryState, int32_t temperature, bool switchPositionChanged, bool supplyVoltageLow, bool fileSizeLimited, uint32_t amplitudeThreshold, AM_filterType_t filterType, uint32_t lowerFilterFreq, uint32_t higherFilterFreq) {

        time_t rawtime = currentTime + timezoneHours * SECONDS_IN_HOUR + timezoneMinutes * SECONDS_IN_MINUTE;

        struct tm *time = gmtime(&rawtime);

        /* Format artist field */

        char *artist = wavHeader->iart.artist;

        sprintf(artist, "AudioMoth %08X%08X", (unsigned int)*((uint32_t*)serialNumber + 1), (unsigned int)*((uint32_t*)serialNumber));

        /* Format comment field */

        char *comment = wavHeader->icmt.comment;

        comment += sprintf(comment, "Recorded at %02d:%02d:%02d %02d/%02d/%04d (UTC", time->tm_hour, time->tm_min, time->tm_sec, time->tm_mday, 1 + time->tm_mon, 1900 + time->tm_year);

        if (timezoneHours < 0) {

            comment += sprintf(comment, "%d", timezoneHours);

        } else if (timezoneHours > 0) {

            comment += sprintf(comment, "+%d", timezoneHours);

        } else {

            if (timezoneMinutes < 0) comment += sprintf(comment, "-%d", timezoneHours);

            if (timezoneMinutes > 0) comment += sprintf(comment, "+%d", timezoneHours);

        }

        if (timezoneMinutes < 0) comment += sprintf(comment, ":%02d", -timezoneMinutes);

        if (timezoneMinutes > 0) comment += sprintf(comment, ":%02d", timezoneMinutes);

        static char *gainSettings[5] = {"low", "low-medium", "medium", "medium-high", "high"};

        comment +=  sprintf(comment, ") by %s at %s gain setting while battery state was ", artist, gainSettings[gain]);

        if (extendedBatteryState == AM_EXT_BAT_LOW) {

            comment += sprintf(comment, "less than 2.5V");

        } else if (extendedBatteryState >= AM_EXT_BAT_FULL) {

            comment += sprintf(comment, "greater than 4.9V");

        } else {

            uint32_t batteryVoltage =  extendedBatteryState + AM_EXT_BAT_STATE_OFFSET / AM_BATTERY_STATE_INCREMENT;

            comment += sprintf(comment, "%01d.%01dV", (unsigned int)batteryVoltage / 10, (unsigned int)batteryVoltage % 10);

        }

        char *sign = temperature < 0 ? "-" : "";

        uint32_t temperatureInDecidegrees = ROUNDED_DIV(ABS(temperature), 100);

        comment += sprintf(comment, " and temperature was %s%d.%dC.", sign, (unsigned int)temperatureInDecidegrees / 10, (unsigned int)temperatureInDecidegrees % 10);

        if (amplitudeThreshold > 0) {

            comment += sprintf(comment, " Amplitude threshold was %d.", (unsigned int)amplitudeThreshold);

        }

        if (filterType == LOW_PASS_FILTER) {

            comment += sprintf(comment, " Low-pass filter applied with cut-off frequency of %01d.%01dkHz.", (unsigned int)higherFilterFreq / 10, (unsigned int)higherFilterFreq % 10);

        } else if (filterType == BAND_PASS_FILTER) {

            comment += sprintf(comment, " Band-pass filter applied with cut-off frequencies of %01d.%01dkHz and %01d.%01dkHz.", (unsigned int)lowerFilterFreq / 10, (unsigned int)lowerFilterFreq % 10, (unsigned int)higherFilterFreq / 10, (unsigned int)higherFilterFreq % 10);

        } else if (filterType == HIGH_PASS_FILTER) {

            comment += sprintf(comment, " High-pass filter applied with cut-off frequency of %01d.%01dkHz.", (unsigned int)lowerFilterFreq / 10, (unsigned int)lowerFilterFreq % 10);

        }

        if (supplyVoltageLow || switchPositionChanged || fileSizeLimited) {

            comment += sprintf(comment, " Recording cancelled before completion due to ");

            if (switchPositionChanged) {

                comment += sprintf(comment, "change of switch position.");

            } else if (supplyVoltageLow) {

                comment += sprintf(comment, "low voltage.");

            } else if (fileSizeLimited) {

                comment += sprintf(comment, "file size limit.");

            }

        }

    }
