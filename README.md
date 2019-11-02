# kafka-event-chaos-injection
Inject exceptions to events to test the resilience of consumers

# Motivation
Test the resilience of the system against faulty events. 
The events should be part of a process to be able to test how features like exception handling and housekeeping behave.

# Idea:
Use the man in the middle attack pattern to modify Kafka events and let the modified events consume by the software under test.
Thus the resilience of the software and of overall solutions should be tested.

Possible modifications:
* delete key value
* change datatype of value
* change value semantically (for example datetime to 01.01.1900)
* replace specific value (for example location 'Berlin' gets replaced by 'Hamburg')
* duplicate event
* etc

# Overview

![](overview.png)

