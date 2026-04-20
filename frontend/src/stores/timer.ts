import { create } from 'zustand'

interface TimerState {
  isRunning: boolean
  timeLeft: number
  totalTime: number
  focusType: 'work' | 'short_break' | 'long_break'
  start: (seconds: number, type: 'work' | 'short_break' | 'long_break') => void
  tick: () => void
  pause: () => void
  reset: () => void
  complete: () => void
}

export const useTimerStore = create<TimerState>((set, get) => ({
  isRunning: false,
  timeLeft: 25 * 60,
  totalTime: 25 * 60,
  focusType: 'work',
  
  start: (seconds, type) => set({
    isRunning: true,
    timeLeft: seconds,
    totalTime: seconds,
    focusType: type
  }),
  
  tick: () => {
    const { timeLeft } = get()
    if (timeLeft > 0) {
      set({ timeLeft: timeLeft - 1 })
    } else {
      set({ isRunning: false })
    }
  },
  
  pause: () => set((s) => ({ isRunning: !s.isRunning })),
  reset: () => set((s) => ({ timeLeft: s.totalTime, isRunning: false })),
  complete: () => set({ isRunning: false })
}))

// Duration presets
export const PRESETS = {
  work: [25, 30, 45, 60],
  short_break: [5, 10],
  long_break: [15, 20, 30]
}
