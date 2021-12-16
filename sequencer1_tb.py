from myhdl import block, always, instance, Signal, ResetSignal, delay, StopSimulation
from sequencer2 import sequencer


@block
def testbench():
    reset = ResetSignal(0, active=1, isasync=True)
    shutdown = Signal(bool(0))
    clk = Signal(bool(0))
    gain = Signal(bool(0))
    ceo = Signal(bool(0))
    start = Signal(bool(1))

    seq1 = sequencer(gain, shutdown, reset, clk, ceo, start)
    seq1.convert(hdl='vhdl')


    HALF_PERIOD = delay(1)

    @always(HALF_PERIOD)
    def clockGen():
        clk.next = not clk

    @instance
    def stimulus():
        for i in range(2):
            yield delay(1000073)
            reset.next = 1
            yield delay(2000)
            reset.next = not reset
            yield delay(20000)
            start.next = 0
            yield delay(70000)
            start.next = 1
        raise StopSimulation()

    return seq1, stimulus, clockGen


tb = testbench()
tb.config_sim(trace=True)
tb.run_sim()
