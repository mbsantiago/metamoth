Diff
~~~~

.. code-block:: diff

    @@ -1,6 +1,6 @@
    -void setHeaderComment(uint32_t currentTime, uint8_t *serialNumber, uint32_t gain) {
    +void setHeaderComment(uint32_t currentTime, int8_t timezone, uint8_t *serialNumber, uint32_t gain) {
     
    -    time_t rawtime = currentTime;
    +    time_t rawtime = currentTime + timezone * SECONDS_IN_HOUR;
     
         struct tm *time = gmtime(&rawtime);
     
    @@ -8,25 +8,35 @@
     
         AM_batteryState_t batteryState = AudioMoth_getBatteryState();
     
    -    sprintf(comment, "Recorded at %02d:%02d:%02d %02d/%02d/%04d (UTC) by AudioMoth %08X%08X at gain setting %d while battery state was ",
    -            time->tm_hour, time->tm_min, time->tm_sec, time->tm_mday, 1 + time->tm_mon, 1900 + time->tm_year,
    -            (unsigned int)(serialNumber + 8), (unsigned int)serialNumber, (unsigned int)gain);
    +    sprintf(comment, "Recorded at %02d:%02d:%02d %02d/%02d/%04d (UTC", time->tm_hour, time->tm_min, time->tm_sec, time->tm_mday, 1 + time->tm_mon, 1900 + time->tm_year);
     
    -    comment += 110;
    +    comment += 36;
    +
    +    if (timezone < 0) sprintf(comment, "%d", timezone);
    +
    +    if (timezone > 0) sprintf(comment, "+%d", timezone);
    +
    +    if (timezone < 0 || timezone > 0) comment += 2;
    +
    +    if (timezone < -9 || timezone > 9) comment += 1;
    +
    +    sprintf(comment, ") by AudioMoth %08X%08X at gain setting %d while battery state was ", (unsigned int)*((uint32_t*)serialNumber + 1), (unsigned int)*((uint32_t*)serialNumber), (unsigned int)gain);
    +
    +    comment += 74;
     
         if (batteryState == AM_BATTERY_LOW) {
     
    -        sprintf(comment, "< 3.6V");
    +        sprintf(comment, "< 3.6V.");
     
         } else if (batteryState >= AM_BATTERY_FULL) {
     
    -        sprintf(comment, "> 5.0V");
    +        sprintf(comment, "> 5.0V.");
     
         } else {
     
             batteryState += 35;
     
    -        sprintf(comment, "%01d.%01dV", batteryState / 10, batteryState % 10);
    +        sprintf(comment, "%01d.%01dV.", batteryState / 10, batteryState % 10);
     
         }
     

Code
~~~~

.. code-block:: C

    void setHeaderComment(uint32_t currentTime, int8_t timezone, uint8_t *serialNumber, uint32_t gain) {

        time_t rawtime = currentTime + timezone * SECONDS_IN_HOUR;

        struct tm *time = gmtime(&rawtime);

        char *comment = wavHeader.icmt.comment;

        AM_batteryState_t batteryState = AudioMoth_getBatteryState();

        sprintf(comment, "Recorded at %02d:%02d:%02d %02d/%02d/%04d (UTC", time->tm_hour, time->tm_min, time->tm_sec, time->tm_mday, 1 + time->tm_mon, 1900 + time->tm_year);

        comment += 36;

        if (timezone < 0) sprintf(comment, "%d", timezone);

        if (timezone > 0) sprintf(comment, "+%d", timezone);

        if (timezone < 0 || timezone > 0) comment += 2;

        if (timezone < -9 || timezone > 9) comment += 1;

        sprintf(comment, ") by AudioMoth %08X%08X at gain setting %d while battery state was ", (unsigned int)*((uint32_t*)serialNumber + 1), (unsigned int)*((uint32_t*)serialNumber), (unsigned int)gain);

        comment += 74;

        if (batteryState == AM_BATTERY_LOW) {

            sprintf(comment, "< 3.6V.");

        } else if (batteryState >= AM_BATTERY_FULL) {

            sprintf(comment, "> 5.0V.");

        } else {

            batteryState += 35;

            sprintf(comment, "%01d.%01dV.", batteryState / 10, batteryState % 10);

        }

    }

