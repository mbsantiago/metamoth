Diff
~~~~

.. code-block:: diff

    @@ -1,12 +1,18 @@
    -void setHeaderComment(uint32_t currentTime, int8_t timezone, uint8_t *serialNumber, uint32_t gain) {
    +void setHeaderComment(uint32_t currentTime, int8_t timezone, uint8_t *serialNumber, uint32_t gain, AM_batteryState_t batteryState, bool batteryVoltageLow, bool switchPositionChanged) {
     
         time_t rawtime = currentTime + timezone * SECONDS_IN_HOUR;
     
         struct tm *time = gmtime(&rawtime);
     
    -    char *comment = wavHeader.icmt.comment;
    +    /* Format artist field */
    +
    +    char *artist = wavHeader.iart.artist;
    +
    +    sprintf(artist, "AudioMoth %08X%08X", (unsigned int)*((uint32_t*)serialNumber + 1), (unsigned int)*((uint32_t*)serialNumber));
     
    -    AM_batteryState_t batteryState = AudioMoth_getBatteryState();
    +    /* Format comment field */
    +
    +    char *comment = wavHeader.icmt.comment;
     
         sprintf(comment, "Recorded at %02d:%02d:%02d %02d/%02d/%04d (UTC", time->tm_hour, time->tm_min, time->tm_sec, time->tm_mday, 1 + time->tm_mon, 1900 + time->tm_year);
     
    @@ -20,17 +26,21 @@
     
         if (timezone < -9 || timezone > 9) comment += 1;
     
    -    sprintf(comment, ") by AudioMoth %08X%08X at gain setting %d while battery state was ", (unsigned int)*((uint32_t*)serialNumber + 1), (unsigned int)*((uint32_t*)serialNumber), (unsigned int)gain);
    +    sprintf(comment, ") by %s at gain setting %d while battery state was ", artist, (unsigned int)gain);
     
         comment += 74;
     
         if (batteryState == AM_BATTERY_LOW) {
     
    -        sprintf(comment, "< 3.6V.");
    +        sprintf(comment, "less than 3.6V.");
    +
    +        comment += 15;
     
         } else if (batteryState >= AM_BATTERY_FULL) {
     
    -        sprintf(comment, "> 5.0V.");
    +        sprintf(comment, "greater than 4.9V.");
    +
    +        comment += 18;
     
         } else {
     
    @@ -38,6 +48,26 @@
     
             sprintf(comment, "%01d.%01dV.", batteryState / 10, batteryState % 10);
     
    +        comment += 5;
    +
    +    }
    +
    +    if (batteryVoltageLow || switchPositionChanged) {
    +
    +        sprintf(comment, " Recording cancelled before completion due to ");
    +
    +        comment += 46;
    +
    +        if (batteryVoltageLow) {
    +
    +            sprintf(comment, "low battery voltage.");
    +
    +        } else if (switchPositionChanged) {
    +
    +            sprintf(comment, "change of switch position.");
    +
    +        }
    +
         }
     
     }

Code
~~~~

.. code-block:: C

    void setHeaderComment(uint32_t currentTime, int8_t timezone, uint8_t *serialNumber, uint32_t gain, AM_batteryState_t batteryState, bool batteryVoltageLow, bool switchPositionChanged) {

        time_t rawtime = currentTime + timezone * SECONDS_IN_HOUR;

        struct tm *time = gmtime(&rawtime);

        /* Format artist field */

        char *artist = wavHeader.iart.artist;

        sprintf(artist, "AudioMoth %08X%08X", (unsigned int)*((uint32_t*)serialNumber + 1), (unsigned int)*((uint32_t*)serialNumber));

        /* Format comment field */

        char *comment = wavHeader.icmt.comment;

        sprintf(comment, "Recorded at %02d:%02d:%02d %02d/%02d/%04d (UTC", time->tm_hour, time->tm_min, time->tm_sec, time->tm_mday, 1 + time->tm_mon, 1900 + time->tm_year);

        comment += 36;

        if (timezone < 0) sprintf(comment, "%d", timezone);

        if (timezone > 0) sprintf(comment, "+%d", timezone);

        if (timezone < 0 || timezone > 0) comment += 2;

        if (timezone < -9 || timezone > 9) comment += 1;

        sprintf(comment, ") by %s at gain setting %d while battery state was ", artist, (unsigned int)gain);

        comment += 74;

        if (batteryState == AM_BATTERY_LOW) {

            sprintf(comment, "less than 3.6V.");

            comment += 15;

        } else if (batteryState >= AM_BATTERY_FULL) {

            sprintf(comment, "greater than 4.9V.");

            comment += 18;

        } else {

            batteryState += 35;

            sprintf(comment, "%01d.%01dV.", batteryState / 10, batteryState % 10);

            comment += 5;

        }

        if (batteryVoltageLow || switchPositionChanged) {

            sprintf(comment, " Recording cancelled before completion due to ");

            comment += 46;

            if (batteryVoltageLow) {

                sprintf(comment, "low battery voltage.");

            } else if (switchPositionChanged) {

                sprintf(comment, "change of switch position.");

            }

        }

    }
