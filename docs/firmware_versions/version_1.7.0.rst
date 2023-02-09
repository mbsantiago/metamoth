Diff
~~~~

.. code-block:: diff

    --- 1.6.0
    +++ 1.7.0
    @@ -72,7 +72,7 @@
     
             uint32_t batteryVoltage =  extendedBatteryState + AM_EXT_BAT_STATE_OFFSET / AM_BATTERY_STATE_INCREMENT;
     
    -        comment += sprintf(comment, "%01ld.%01ldV", batteryVoltage / 10, batteryVoltage % 10);
    +        comment += sprintf(comment, "%01lu.%01luV", batteryVoltage / 10, batteryVoltage % 10);
     
         }
     
    @@ -80,7 +80,7 @@
     
         uint32_t temperatureInDecidegrees = ROUNDED_DIV(ABS(temperature), 100);
     
    -    comment += sprintf(comment, " and temperature was %s%ld.%ldC.", sign, temperatureInDecidegrees / 10, temperatureInDecidegrees % 10);
    +    comment += sprintf(comment, " and temperature was %s%lu.%luC.", sign, temperatureInDecidegrees / 10, temperatureInDecidegrees % 10);
         
         bool amplitudeThresholdEnabled = configSettings->amplitudeThreshold > 0 || configSettings->enableAmplitudeThresholdDecibelScale || configSettings->enableAmplitudeThresholdPercentageScale;
     
    @@ -96,11 +96,11 @@
     
         } else if (amplitudeThresholdEnabled) {
     
    -        comment += sprintf(comment, "%d", configSettings->amplitudeThreshold);
    +        comment += sprintf(comment, "%u", configSettings->amplitudeThreshold);
     
         }
     
    -    if (amplitudeThresholdEnabled) comment += sprintf(comment, " with %ds minimum trigger duration.", configSettings->minimumTriggerDuration);
    +    if (amplitudeThresholdEnabled) comment += sprintf(comment, " with %us minimum trigger duration.", configSettings->minimumTriggerDuration);
     
         uint16_t lowerFilterFreq = configSettings->lowerFilterFreq;
     
    @@ -108,37 +108,41 @@
     
         if (filterType == LOW_PASS_FILTER) {
     
    -        comment += sprintf(comment, " Low-pass filter with frequency of %01d.%01dkHz applied.", higherFilterFreq / 10, higherFilterFreq % 10);
    +        comment += sprintf(comment, " Low-pass filter with frequency of %01u.%01ukHz applied.", higherFilterFreq / 10, higherFilterFreq % 10);
     
         } else if (filterType == BAND_PASS_FILTER) {
     
    -        comment += sprintf(comment, " Band-pass filter with frequencies of %01d.%01dkHz and %01d.%01dkHz applied.", lowerFilterFreq / 10, lowerFilterFreq % 10, higherFilterFreq / 10, higherFilterFreq % 10);
    +        comment += sprintf(comment, " Band-pass filter with frequencies of %01u.%01ukHz and %01u.%01ukHz applied.", lowerFilterFreq / 10, lowerFilterFreq % 10, higherFilterFreq / 10, higherFilterFreq % 10);
     
         } else if (filterType == HIGH_PASS_FILTER) {
     
    -        comment += sprintf(comment, " High-pass filter with frequency of %01d.%01dkHz applied.", lowerFilterFreq / 10, lowerFilterFreq % 10);
    +        comment += sprintf(comment, " High-pass filter with frequency of %01u.%01ukHz applied.", lowerFilterFreq / 10, lowerFilterFreq % 10);
     
         }
     
         if (recordingState != RECORDING_OKAY) {
     
    -        comment += sprintf(comment, " Recording stopped due to ");
    +        comment += sprintf(comment, " Recording stopped");
     
             if (recordingState == MICROPHONE_CHANGED) {
     
    -            comment += sprintf(comment, "microphone change.");
    +            comment += sprintf(comment, " due to microphone change.");
     
             } else if (recordingState == SWITCH_CHANGED) {
     
    -            comment += sprintf(comment, "switch position change.");
    +            comment += sprintf(comment, " due to switch position change.");
    +
    +        } else if (recordingState == MAGNETIC_SWITCH) {
    +        
    +            comment += sprintf(comment, " by magnetic switch.");
     
             } else if (recordingState == SUPPLY_VOLTAGE_LOW) {
     
    -            comment += sprintf(comment, "low voltage.");
    +            comment += sprintf(comment, " due to low voltage.");
     
             } else if (recordingState == FILE_SIZE_LIMITED) {
     
    -            comment += sprintf(comment, "file size limit.");
    +            comment += sprintf(comment, " due to file size limit.");
     
             }
     

Code
~~~~

.. code-block:: C

    static void setHeaderComment(wavHeader_t *wavHeader, configSettings_t *configSettings, uint32_t currentTime, uint8_t *serialNumber, uint8_t *deploymentID, uint8_t *defaultDeploymentID, AM_extendedBatteryState_t extendedBatteryState, int32_t temperature, bool externalMicrophone, AM_recordingState_t recordingState, AM_filterType_t filterType) {

        time_t rawTime = currentTime + configSettings->timezoneHours * SECONDS_IN_HOUR + configSettings->timezoneMinutes * SECONDS_IN_MINUTE;

        struct tm *time = gmtime(&rawTime);

        /* Format artist field */

        char *artist = wavHeader->iart.artist;

        sprintf(artist, "AudioMoth " SERIAL_NUMBER, FORMAT_SERIAL_NUMBER(serialNumber));

        /* Format comment field */

        char *comment = wavHeader->icmt.comment;

        comment += sprintf(comment, "Recorded at %02d:%02d:%02d %02d/%02d/%04d (UTC", time->tm_hour, time->tm_min, time->tm_sec, time->tm_mday, 1 + time->tm_mon, 1900 + time->tm_year);

        int8_t timezoneHours = configSettings->timezoneHours;

        int8_t timezoneMinutes = configSettings->timezoneMinutes;

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

        comment += sprintf(comment, "at %s gain while battery was ", gainSettings[configSettings->gain]);

        if (extendedBatteryState == AM_EXT_BAT_LOW) {

            comment += sprintf(comment, "less than 2.5V");

        } else if (extendedBatteryState >= AM_EXT_BAT_FULL) {

            comment += sprintf(comment, "greater than 4.9V");

        } else {

            uint32_t batteryVoltage =  extendedBatteryState + AM_EXT_BAT_STATE_OFFSET / AM_BATTERY_STATE_INCREMENT;

            comment += sprintf(comment, "%01lu.%01luV", batteryVoltage / 10, batteryVoltage % 10);

        }

        char *sign = temperature < 0 ? "-" : "";

        uint32_t temperatureInDecidegrees = ROUNDED_DIV(ABS(temperature), 100);

        comment += sprintf(comment, " and temperature was %s%lu.%luC.", sign, temperatureInDecidegrees / 10, temperatureInDecidegrees % 10);
        
        bool amplitudeThresholdEnabled = configSettings->amplitudeThreshold > 0 || configSettings->enableAmplitudeThresholdDecibelScale || configSettings->enableAmplitudeThresholdPercentageScale;

        if (amplitudeThresholdEnabled) comment += sprintf(comment, " Amplitude threshold was ");

        if (configSettings->enableAmplitudeThresholdDecibelScale && configSettings->enableAmplitudeThresholdPercentageScale == false) {

            comment += formatDecibels(comment, configSettings->amplitudeThresholdDecibels);

        } else if (configSettings->enableAmplitudeThresholdPercentageScale && configSettings->enableAmplitudeThresholdDecibelScale == false) {

            comment += formatPercentage(comment, configSettings->amplitudeThresholdPercentageMantissa, configSettings->amplitudeThresholdPercentageExponent);

        } else if (amplitudeThresholdEnabled) {

            comment += sprintf(comment, "%u", configSettings->amplitudeThreshold);

        }

        if (amplitudeThresholdEnabled) comment += sprintf(comment, " with %us minimum trigger duration.", configSettings->minimumTriggerDuration);

        uint16_t lowerFilterFreq = configSettings->lowerFilterFreq;

        uint16_t higherFilterFreq = configSettings->higherFilterFreq;

        if (filterType == LOW_PASS_FILTER) {

            comment += sprintf(comment, " Low-pass filter with frequency of %01u.%01ukHz applied.", higherFilterFreq / 10, higherFilterFreq % 10);

        } else if (filterType == BAND_PASS_FILTER) {

            comment += sprintf(comment, " Band-pass filter with frequencies of %01u.%01ukHz and %01u.%01ukHz applied.", lowerFilterFreq / 10, lowerFilterFreq % 10, higherFilterFreq / 10, higherFilterFreq % 10);

        } else if (filterType == HIGH_PASS_FILTER) {

            comment += sprintf(comment, " High-pass filter with frequency of %01u.%01ukHz applied.", lowerFilterFreq / 10, lowerFilterFreq % 10);

        }

        if (recordingState != RECORDING_OKAY) {

            comment += sprintf(comment, " Recording stopped");

            if (recordingState == MICROPHONE_CHANGED) {

                comment += sprintf(comment, " due to microphone change.");

            } else if (recordingState == SWITCH_CHANGED) {

                comment += sprintf(comment, " due to switch position change.");

            } else if (recordingState == MAGNETIC_SWITCH) {
            
                comment += sprintf(comment, " by magnetic switch.");

            } else if (recordingState == SUPPLY_VOLTAGE_LOW) {

                comment += sprintf(comment, " due to low voltage.");

            } else if (recordingState == FILE_SIZE_LIMITED) {

                comment += sprintf(comment, " due to file size limit.");

            }

        }

    }

