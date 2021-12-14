from myhdl import always_seq, enum, modbv, block, Signal

ACTIVE_HIGH = 1

@block
def sequencer(gain, shutdown, reset, clk, ceo, start):
    t_state = enum('A_5', 'Fis_5', 'G_5', 'A_4', 'B_4', 'Cis_5', 'D_5', 'E_5')
    state = Signal(t_state.A_5)
    sounds = [11, 13, 12, 22, 19, 18, 17, 15]
    sounds_divider = [Signal(modbv(1, min=0, max=sounds[i])) for i in range(len(sounds))]
    length = [46, 19, 21, 11, 13, 14, 15, 17, 23]
    length_divider = [Signal(modbv(1, min=0, max=length[i])) for i in range(len(length))]
    ceo_sig = Signal(0)
    iteration = Signal(modbv(0, min=0, max=3))

    def func(sounds_divider1, ceo_sig1, length_divider1, state1, t_state1):
        if sounds_divider1 == 0:
            if ceo_sig1 == 1:
                if length_divider1 == 0:
                    state1.next = t_state1
                length_divider1.next = length_divider1 + 1
            ceo_sig1.next = not ceo_sig1
        sounds_divider1.next = sounds_divider1 + 1

    @always_seq(clk.posedge, reset=reset)
    def seq_logic():
        gain.next = 1
        shutdown.next = 1
        if reset == ACTIVE_HIGH:
            state.next = t_state.A_5
            sounds_divider.next = [1 for i in range(len(sounds_divider))]
            ceo_sig.next = 0
            iteration.next = 0
            length_divider.next = [1 for i in range(len(length_divider))]
        else:
            if start == 1:
                if state == t_state.A_5:
                    if sounds_divider[0] == 0:
                        if ceo_sig == 1:
                            if iteration < 2:
                                if length_divider[0] == 0:
                                    state.next = t_state.Fis_5
                                    iteration.next = iteration + 1
                                length_divider[0].next = length_divider[0] + 1
                            else:
                                if length_divider[8] == 0:
                                    state.next = t_state.A_4
                                    iteration.next = iteration + 1
                                length_divider[8].next = length_divider[8] + 1
                        ceo_sig.next = not ceo_sig
                    sounds_divider[0].next = sounds_divider[0] + 1
                elif state == t_state.Fis_5:
                    func(sounds_divider[1], ceo_sig, length_divider[1], state, t_state.G_5)
                elif state == t_state.G_5:
                    func(sounds_divider[2], ceo_sig, length_divider[2], state, t_state.A_5)
                elif state == t_state.A_4:
                    func(sounds_divider[3], ceo_sig, length_divider[3], state, t_state.B_4)
                elif state == t_state.B_4:
                    func(sounds_divider[4], ceo_sig, length_divider[4], state, t_state.Cis_5)
                elif state == t_state.Cis_5:
                    func(sounds_divider[5], ceo_sig, length_divider[5], state, t_state.D_5)
                elif state == t_state.D_5:
                    func(sounds_divider[6], ceo_sig, length_divider[6], state, t_state.E_5)
                elif state == t_state.E_5:
                    func(sounds_divider[7], ceo_sig, length_divider[7], state, t_state.Fis_5)
        ceo.next = ceo_sig
    return seq_logic


