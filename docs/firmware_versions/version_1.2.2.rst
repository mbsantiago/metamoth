Diff
~~~~

.. code-block:: diff

    @@ -1,6 +1,6 @@
    -void setHeaderComment(uint32_t currentTime, int8_t timezone, uint8_t *serialNumber, uint32_t gain, AM_batteryState_t batteryState, bool batteryVoltageLow, bool switchPositionChanged) {
    +void setHeaderComment(uint32_t currentTime, int8_t timezoneHours, int8_t timezoneMinutes, uint8_t *serialNumber, uint32_t gain, AM_batteryState_t batteryState, bool batteryVoltageLow, bool switchPositionChanged) {
     
    -    time_t rawtime = currentTime + timezone * SECONDS_IN_HOUR;
    +    time_t rawtime = currentTime + timezoneHours * SECONDS_IN_HOUR + timezoneMinutes * SECONDS_IN_MINUTE;
     
         struct tm *time = gmtime(&rawtime);
     
    @@ -18,13 +18,19 @@
     
         comment += 36;
     
    -    if (timezone < 0) sprintf(comment, "%d", timezone);
    +    if (timezoneHours < 0) sprintf(comment, "%d", timezoneHours);
     
    -    if (timezone > 0) sprintf(comment, "+%d", timezone);
    +    if (timezoneHours > 0) sprintf(comment, "+%d", timezoneHours);
     
    -    if (timezone < 0 || timezone > 0) comment += 2;
    +    if (timezoneHours < 0 || timezoneHours > 0) comment += 2;
     
    -    if (timezone < -9 || timezone > 9) comment += 1;
    +    if (timezoneHours < -9 || timezoneHours > 9) comment += 1;
    +
    +    if (timezoneMinutes < 0) sprintf(comment, ":%2d", -timezoneMinutes);
    +
    +    if (timezoneMinutes > 0) sprintf(comment, ":%2d", timezoneMinutes);
    +
    +    if (timezoneMinutes < 0 || timezoneMinutes > 0) comment += 3;
     
         sprintf(comment, ") by %s at gain setting %d while battery state was ", artist, (unsigned int)gain);
     

Code
~~~~

.. code-block:: C

    void setHeaderComment(uint32_t currentTime, int8_t timezoneHours, int8_t timezoneMinutes, uint8_t *serialNumber, uint32_t gain, AM_batteryState_t batteryState, bool batteryVoltageLow, bool switchPositionChanged) {

        time_t rawtime = currentTime + timezoneHours * SECONDS_IN_HOUR + timezoneMinutes * SECONDS_IN_MINUTE;

        struct tm *time = gmtime(&rawtime);

        /* Format artist field */

        char *artist = wavHeader.iart.artist;

        sprintf(artist, "AudioMoth %08X%08X", (unsigned int)*((uint32_t*)serialNumber + 1), (unsigned int)*((uint32_t*)serialNumber));

        /* Format comment field */

        char *comment = wavHeader.icmt.comment;

        sprintf(comment, "Recorded at %02d:%02d:%02d %02d/%02d/%04d (UTC", time->tm_hour, time->tm_min, time->tm_sec, time->tm_mday, 1 + time->tm_mon, 1900 + time->tm_year);

        comment += 36;

        if (timezoneHours < 0) sprintf(comment, "%d", timezoneHours);

        if (timezoneHours > 0) sprintf(comment, "+%d", timezoneHours);

        if (timezoneHours < 0 || timezoneHours > 0) comment += 2;

        if (timezoneHours < -9 || timezoneHours > 9) comment += 1;

        if (timezoneMinutes < 0) sprintf(comment, ":%2d", -timezoneMinutes);

        if (timezoneMinutes > 0) sprintf(comment, ":%2d", timezoneMinutes);

        if (timezoneMinutes < 0 || timezoneMinutes > 0) comment += 3;

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
