# bonsai-osc-bidirectional-example
Sending data back and forth between bonsai and a pyqt python program via Osc


This is a minimal pretty unoptimized example of how to do this. The only nontrivial things are how to set up the required servers/clients on both sides, and how to throw the server on the python side in its own thread.

There are likely a few things wrong with this - this is just the first working code I manged to put together with no clean up or optimization.

Requires pyqt6, and python-osc ( https://python-osc.readthedocs.io/en/latest/index.html ).
There's likely a few other requirements but this is pretty minimal.

Relevant discussions are also here: https://github.com/bonsai-rx/bonsai/discussions/872

ALso see Spencer Blackwood's solution: https://github.com/spencerblackwood/bonsai-osc-jupyter-example