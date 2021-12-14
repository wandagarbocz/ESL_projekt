from myhdl import block, always, instance, Signal, ResetSignal, delay, StopSimulation
from sequencer1 import sequencer


@block
def testbench():
    reset = ResetSignal(0, active=1, isasync=True)
    shutdown = Signal(bool(0))
    clk = Signal(bool(0))
    gain = Signal(bool(0))
    ceo = Signal(bool(0))
    start = Signal(bool(1))

    seq1 = sequencer(gain, shutdown, reset, clk, ceo, start)

    HALF_PERIOD = delay(1)

    @always(HALF_PERIOD)
    def clockGen():
        clk.next = not clk

    @instance
    def stimulus():
        for i in range(10):
            yield delay(40073)
            reset.next = 1
            yield delay(20)
            reset.next = 0
            yield delay(100)
            start.next = 0
            yield delay(200)
            start.next = 1
        raise StopSimulation()

    return seq1, stimulus, clockGen


tb = testbench()
tb.config_sim(trace=True)
tb.run_sim()
