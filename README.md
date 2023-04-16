# noiftimer
Simple timer class to track elapsed time.<br>
Install with:
<pre>pip install noiftimer</pre>

Usage:
<pre>
>>> from noiftimer import Timer, time_it
>>> import time
</pre>
Timer object
<pre>
>>> def very_complicated_function():
...     time.sleep(1)
...
>>> timer = Timer()
>>> for _ in range(10):
...     timer.start()
...     very_complicated_function()
...     timer.stop()
...
>>> print(timer.stats)
elapsed time: 1s 1ms 173us
average elapsed time: 1s 912us
>>> timer.elapsed
1.001173496246338
>>> timer.elapsed_str
'1s 1ms 173us'
>>> timer.average_elapsed
1.0009121656417848
>>> timer.average_elapsed_str
'1s 912us'
</pre>
time_it decorator (executes the decorated function 10 times)
<pre>
>>> @time_it(10)
... def very_complicated_function():
...     time.sleep(1)
...
>>> very_complicated_function()
very_complicated_function average execution time: 1s 469us
</pre>
