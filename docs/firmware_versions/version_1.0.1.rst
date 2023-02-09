Diff
~~~~

.. code-block:: diff

    @@ -8,11 +8,11 @@

         AM_batteryState_t batteryState = AudioMoth_getBatteryState();

    -    sprintf(comment, "Recorded at %02d:%02d:%02d %02d/%02d/%04d by AudioMoth %08X%08X at gain setting %d while battery state was ",
    +    sprintf(comment, "Recorded at %02d:%02d:%02d %02d/%02d/%04d (UTC) by AudioMoth %08X%08X at gain setting %d while battery state was ",
                 time->tm_hour, time->tm_min, time->tm_sec, time->tm_mday, 1 + time->tm_mon, 1900 + time->tm_year,
                 (unsigned int)(serialNumber + 8), (unsigned int)serialNumber, (unsigned int)gain);

    -    comment += 104;
    +    comment += 110;

         if (batteryState == AM_BATTERY_LOW) {

    @@ -26,10 +26,7 @@

             batteryState += 35;

    -        int tens = batteryState / 10;
    -        int units = batteryState - 10 * tens;
    -
    -        sprintf(comment, "%01d.%02dV", tens, units);
    +        sprintf(comment, "%01d.%01dV", batteryState / 10, batteryState % 10);

         }

Code
~~~~

.. code-block:: C

    void setHeaderComment(uint32_t currentTime, uint8_t *serialNumber, uint32_t gain) {

        time_t rawtime = currentTime;

        struct tm *time = gmtime(&rawtime);

        char *comment = wavHeader.icmt.comment;

        AM_batteryState_t batteryState = AudioMoth_getBatteryState();

        sprintf(comment, "Recorded at %02d:%02d:%02d %02d/%02d/%04d (UTC) by AudioMoth %08X%08X at gain setting %d while battery state was ",
                time->tm_hour, time->tm_min, time->tm_sec, time->tm_mday, 1 + time->tm_mon, 1900 + time->tm_year,
                (unsigned int)(serialNumber + 8), (unsigned int)serialNumber, (unsigned int)gain);

        comment += 110;

        if (batteryState == AM_BATTERY_LOW) {

            sprintf(comment, "< 3.6V");

        } else if (batteryState >= AM_BATTERY_FULL) {

            sprintf(comment, "> 5.0V");

        } else {

            batteryState += 35;

            sprintf(comment, "%01d.%01dV", batteryState / 10, batteryState % 10);

        }

    }

