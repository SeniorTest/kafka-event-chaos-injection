# kafka-event-chaos-injection
Inject exceptions to events to test the resilience of consumers


# Idea:
Use the man in the middle attack pattern to modify Kafka events and let the modified events consume by the software under test.
Thus the resilience of the software and of overall solutions should be tested.


