from myhdl import always_seq, enum, modbv, block, Signal, intbv

ACTIVE_HIGH = 1

@block
def sequencer(gain, shutdown, reset, clk, ceo, start):
    t_state = enum('A_5', 'Fis_5', 'G_5', 'A_4', 'B_4', 'Cis_5', 'D_5', 'E_5')
    state = Signal(t_state.A_5)
    sounds = [33, 43, 38, 64, 60, 57, 53, 48]#[11, 13, 12, 22, 19, 18, 17, 15]
    sounds_divider = [Signal(modbv(1, min=0, max=sounds[i])[7:]) for i in range(len(sounds))]
    length = [31, 17, 17, 17, 17, 17, 17, 17, 17]#[46, 19, 21, 11, 13, 14, 15, 17, 23]
    length_divider = [Signal(modbv(1, min=0, max=length[i])[5:]) for i in range(len(length))]
    ceo_sig = Signal(bool(0))
    #iteration = Signal(modbv(13, min=13, max=16))
    iteration = Signal(modbv(0, min=0, max=2)[2:])


    @always_seq(clk.posedge, reset=reset)
    def seq_logic():
        gain.next = 1
        shutdown.next = 1
        if reset == ACTIVE_HIGH:
            state.next = t_state.A_5
            for i in range(len(sounds_divider)):
                sounds_divider[i].next = 1#Signal(intbv(1)[len(sounds_divider):])# for i in range(len(sounds_divider))]
            ceo_sig.next = 0
            iteration.next = 0
            for i in range(len(length_divider)):
                length_divider[i].next = 1#Signal(intbv(1)[len(length_divider):])#[1 for i in range(len(length_divider))]
        else:
            if start == ACTIVE_HIGH:
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
                                    iteration.next = 0
                                length_divider[8].next = length_divider[8] + 1
                        ceo_sig.next = not ceo_sig
                    sounds_divider[0].next = sounds_divider[0] + 1
                elif state == t_state.Fis_5:
                    if sounds_divider[1] == 0:
                        if ceo_sig == 1:
                            if length_divider[1] == 0:
                                state.next = t_state.G_5
                            length_divider[1].next = length_divider[1] + 1
                        ceo_sig.next = not ceo_sig
                    sounds_divider[1].next = sounds_divider[1] + 1
                elif state == t_state.G_5:
                    if sounds_divider[2] == 0:
                        if ceo_sig == 1:
                            if length_divider[2] == 0:
                                state.next = t_state.A_5
                            length_divider[2].next = length_divider[2] + 1
                        ceo_sig.next = not ceo_sig
                    sounds_divider[2].next = sounds_divider[2] + 1
                elif state == t_state.A_4:
                    if sounds_divider[3] == 0:
                        if ceo_sig == 1:
                            if length_divider[3] == 0:
                                state.next = t_state.B_4
                            length_divider[3].next = length_divider[3] + 1
                        ceo_sig.next = not ceo_sig
                    sounds_divider[3].next = sounds_divider[3] + 1
                elif state == t_state.B_4:
                    if sounds_divider[4] == 0:
                        if ceo_sig == 1:
                            if length_divider[4] == 0:
                                state.next = t_state.Cis_5
                            length_divider[4].next = length_divider[4] + 1
                        ceo_sig.next = not ceo_sig
                    sounds_divider[4].next = sounds_divider[4] + 1
                elif state == t_state.Cis_5:
                    if sounds_divider[5] == 0:
                        if ceo_sig == 1:
                            if length_divider[5] == 0:
                                state.next = t_state.D_5
                            length_divider[5].next = length_divider[5] + 1
                        ceo_sig.next = not ceo_sig
                    sounds_divider[5].next = sounds_divider[5] + 1
                elif state == t_state.D_5:
                    if sounds_divider[6] == 0:
                        if ceo_sig == 1:
                            if length_divider[6] == 0:
                                state.next = t_state.E_5
                            length_divider[6].next = length_divider[6] + 1
                        ceo_sig.next = not ceo_sig
                    sounds_divider[6].next = sounds_divider[6] + 1
                elif state == t_state.E_5:
                    if sounds_divider[7] == 0:
                        if ceo_sig == 1:
                            if length_divider[7] == 0:
                                state.next = t_state.Fis_5
                            length_divider[7].next = length_divider[7] + 1
                        ceo_sig.next = not ceo_sig
                    sounds_divider[7].next = sounds_divider[7] + 1
        ceo.next = ceo_sig
    return seq_logic
