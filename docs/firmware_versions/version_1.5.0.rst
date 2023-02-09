Diff
~~~~

.. code-block:: diff

    @@ -1,4 +1,4 @@
    -static void setHeaderComment(wavHeader_t *wavHeader, uint32_t currentTime, int8_t timezoneHours, int8_t timezoneMinutes, uint8_t *serialNumber, uint32_t gain, AM_extendedBatteryState_t extendedBatteryState, int32_t temperature, bool switchPositionChanged, bool supplyVoltageLow, bool fileSizeLimited, uint32_t amplitudeThreshold, AM_filterType_t filterType, uint32_t lowerFilterFreq, uint32_t higherFilterFreq) {
    +static void setHeaderComment(wavHeader_t *wavHeader, uint32_t currentTime, int8_t timezoneHours, int8_t timezoneMinutes, uint8_t *serialNumber, uint8_t *deploymentID, uint8_t *defaultDeploymentID, uint32_t gain, AM_extendedBatteryState_t extendedBatteryState, int32_t temperature, bool externalMicrophone, AM_recordingState_t recordingState, uint32_t amplitudeThreshold, AM_filterType_t filterType, uint32_t lowerFilterFreq, uint32_t higherFilterFreq) {
     
         time_t rawtime = currentTime + timezoneHours * SECONDS_IN_HOUR + timezoneMinutes * SECONDS_IN_MINUTE;
     
    @@ -8,7 +8,7 @@
     
         char *artist = wavHeader->iart.artist;
     
    -    sprintf(artist, "AudioMoth %08X%08X", (unsigned int)*((uint32_t*)serialNumber + 1), (unsigned int)*((uint32_t*)serialNumber));
    +    sprintf(artist, "AudioMoth " SERIAL_NUMBER, FORMAT_SERIAL_NUMBER(serialNumber));
     
         /* Format comment field */
     
    @@ -36,9 +36,25 @@
     
         if (timezoneMinutes > 0) comment += sprintf(comment, ":%02d", timezoneMinutes);
     
    +    if (memcmp(deploymentID, defaultDeploymentID, DEPLOYMENT_ID_LENGTH)) {
    +
    +        comment += sprintf(comment, ") during deployment " SERIAL_NUMBER " ", FORMAT_SERIAL_NUMBER(deploymentID));
    +
    +    } else {
    +
    +        comment += sprintf(comment, ") by %s ", artist);
    +
    +    }
    +
    +    if (externalMicrophone) {
    +
    +        comment += sprintf(comment, "using external microphone ");
    +
    +    }
    +
         static char *gainSettings[5] = {"low", "low-medium", "medium", "medium-high", "high"};
     
    -    comment +=  sprintf(comment, ") by %s at %s gain setting while battery state was ", artist, gainSettings[gain]);
    +    comment += sprintf(comment, "at %s gain setting while battery state was ", gainSettings[gain]);
     
         if (extendedBatteryState == AM_EXT_BAT_LOW) {
     
    @@ -82,19 +98,23 @@
     
         }
     
    -    if (supplyVoltageLow || switchPositionChanged || fileSizeLimited) {
    +    if (recordingState != RECORDING_OKAY) {
     
             comment += sprintf(comment, " Recording cancelled before completion due to ");
     
    -        if (switchPositionChanged) {
    +        if (recordingState == MICROPHONE_CHANGED) {
    +
    +            comment += sprintf(comment, "microphone change.");
    +
    +        } else if (recordingState == SWITCH_CHANGED) {
     
                 comment += sprintf(comment, "change of switch position.");
     
    -        } else if (supplyVoltageLow) {
    +        } else if (recordingState == SUPPLY_VOLTAGE_LOW) {
     
                 comment += sprintf(comment, "low voltage.");
     
    -        } else if (fileSizeLimited) {
    +        } else if (recordingState == FILE_SIZE_LIMITED) {
     
                 comment += sprintf(comment, "file size limit.");
     

Code
~~~~

.. code-block:: C

    static void setHeaderComment(wavHeader_t *wavHeader, uint32_t currentTime, int8_t timezoneHours, int8_t timezoneMinutes, uint8_t *serialNumber, uint8_t *deploymentID, uint8_t *defaultDeploymentID, uint32_t gain, AM_extendedBatteryState_t extendedBatteryState, int32_t temperature, bool externalMicrophone, AM_recordingState_t recordingState, uint32_t amplitudeThreshold, AM_filterType_t filterType, uint32_t lowerFilterFreq, uint32_t higherFilterFreq) {

        time_t rawtime = currentTime + timezoneHours * SECONDS_IN_HOUR + timezoneMinutes * SECONDS_IN_MINUTE;

        struct tm *time = gmtime(&rawtime);

        /* Format artist field */

        char *artist = wavHeader->iart.artist;

        sprintf(artist, "AudioMoth " SERIAL_NUMBER, FORMAT_SERIAL_NUMBER(serialNumber));

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

        if (memcmp(deploymentID, defaultDeploymentID, DEPLOYMENT_ID_LENGTH)) {

            comment += sprintf(comment, ") during deployment " SERIAL_NUMBER " ", FORMAT_SERIAL_NUMBER(deploymentID));

        } else {

            comment += sprintf(comment, ") by %s ", artist);

        }

        if (externalMicrophone) {

            comment += sprintf(comment, "using external microphone ");

        }

        static char *gainSettings[5] = {"low", "low-medium", "medium", "medium-high", "high"};

        comment += sprintf(comment, "at %s gain setting while battery state was ", gainSettings[gain]);

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

        if (recordingState != RECORDING_OKAY) {

            comment += sprintf(comment, " Recording cancelled before completion due to ");

            if (recordingState == MICROPHONE_CHANGED) {

                comment += sprintf(comment, "microphone change.");

            } else if (recordingState == SWITCH_CHANGED) {

                comment += sprintf(comment, "change of switch position.");

            } else if (recordingState == SUPPLY_VOLTAGE_LOW) {

                comment += sprintf(comment, "low voltage.");

            } else if (recordingState == FILE_SIZE_LIMITED) {

                comment += sprintf(comment, "file size limit.");

            }

        }

    }
