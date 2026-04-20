import { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '../stores/auth'
import { useTimerStore, PRESETS } from '../stores/timer'
import { focusApi, soundsApi, achievementsApi } from '../services/api'

export default function Dashboard() {
  const user = useAuthStore((s) => s.user)
  const logout = useAuthStore((s) => s.logout)
  const navigate = useNavigate()
  
  const { isRunning, timeLeft, totalTime, focusType, start, tick, pause, reset } = useTimerStore()
  const [currentSession, setCurrentSession] = useState<number | null>(null)
  const [sounds, setSounds] = useState<any[]>([])
  const [achievements, setAchievements] = useState<any[]>([])
  const [selectedSound, setSelectedSound] = useState<string | null>(null)
  const [showStats, setShowStats] = useState(false)
  const [dailyStats, setDailyStats] = useState<any[]>([])
  
  const audioRef = useRef<HTMLAudioElement | null>(null)
  const intervalRef = useRef<NodeJS.Timeout | null>(null)

  useEffect(() => {
    loadData()
  }, [])

  useEffect(() => {
    if (isRunning) {
      intervalRef.current = setInterval(() => {
        tick()
      }, 1000)
    } else {
      if (intervalRef.current) clearInterval(intervalRef.current)
    }
    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current)
    }
  }, [isRunning, tick])

  useEffect(() => {
    if (timeLeft === 0 && currentSession) {
      handleComplete(true)
    }
  }, [timeLeft])

  const loadData = async () => {
    try {
      const [soundsRes, achRes, dailyRes] = await Promise.all([
        soundsApi.list(),
        achievementsApi.earned(),
        focusApi.dailyStats()
      ])
      setSounds(soundsRes.data)
      setAchievements(achRes.data)
      setDailyStats(dailyRes.data)
    } catch (e) {
      console.error(e)
    }
  }

  const formatTime = (seconds: number) => {
    const m = Math.floor(seconds / 60)
    const s = seconds % 60
    return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
  }

  const handleStart = async (minutes: number, type: 'work' | 'short_break' | 'long_break') => {
    try {
      if (type === 'work') {
        const res = await focusApi.start({ focus_type: type, duration_minutes: minutes })
        setCurrentSession(res.data.id)
      }
      start(minutes * 60, type)
    } catch (e) {
      console.error(e)
    }
  }

  const handleComplete = async (completed: boolean) => {
    if (currentSession && focusType === 'work') {
      try {
        await focusApi.complete(currentSession, completed)
        const me = await useAuthStore.getState().setUser
        // Refresh user data
      } catch (e) {
        console.error(e)
      }
    }
    setCurrentSession(null)
    reset()
  }

  const progress = totalTime > 0 ? ((totalTime - timeLeft) / totalTime) * 100 : 0
  const circumference = 2 * Math.PI * 120
  const strokeDashoffset = circumference - (progress / 100) * circumference

  return (
    <div className="min-h-screen p-4">
      {/* Header */}
      <nav className="flex justify-between items-center mb-8">
        <div className="flex items-center gap-2">
          <span className="text-2xl">鈴憋笍</span>
          <span className="font-bold text-xl">FocusFlow</span>
        </div>
        <div className="flex items-center gap-4">
          <span className="text-yellow-400">馃挵 {user?.coins || 0}</span>
          <span className="text-purple-300">馃敟 {user?.current_streak || 0} days</span>
          <button onClick={() => setShowStats(!showStats)} className="text-purple-400 hover:underline">
            Stats
          </button>
          <button onClick={() => { logout(); navigate('/') }} className="text-gray-400 hover:text-white">
            Logout
          </button>
        </div>
      </nav>

      <main className="max-w-4xl mx-auto">
        {/* Timer Circle */}
        <div className="flex flex-col items-center mb-8">
          <div className="relative w-72 h-72">
            <svg className="w-full h-full transform -rotate-90 timer-ring">
              <circle
                cx="144" cy="144" r="120"
                stroke="rgba(255,255,255,0.1)"
                strokeWidth="12"
                fill="none"
              />
              <circle
                cx="144" cy="144" r="120"
                stroke={focusType === 'work' ? '#a855f7' : '#22c55e'}
                strokeWidth="12"
                fill="none"
                strokeLinecap="round"
                strokeDasharray={circumference}
                strokeDashoffset={strokeDashoffset}
                className="transition-all duration-1000"
              />
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className={`text-5xl font-mono ${isRunning ? 'tick-animation' : ''}`}>
                {formatTime(timeLeft)}
              </span>
              <span className="text-sm text-purple-300 mt-2">
                {focusType === 'work' ? '馃幆 Focus Time' : focusType === 'short_break' ? '鈽?Short Break' : '馃尨 Long Break'}
              </span>
            </div>
          </div>

          {/* Controls */}
          <div className="flex gap-3 mt-6">
            {!isRunning ? (
              <>
                <button onClick={pause} className="px-6 py-2 bg-white/10 hover:bg-white/20 rounded-lg">
                  {isRunning ? '鈴革笍 Pause' : '鈻讹笍 Resume'}
                </button>
                <button onClick={reset} className="px-6 py-2 bg-white/10 hover:bg-white/20 rounded-lg">
                  馃攧 Reset
                </button>
              </>
            ) : (
              <>
                <button onClick={pause} className="px-6 py-2 bg-purple-600 hover:bg-purple-700 rounded-lg">
                  鈴革笍 Pause
                </button>
                <button onClick={() => handleComplete(false)} className="px-6 py-2 bg-red-600/50 hover:bg-red-600 rounded-lg">
                  鉁?Skip
                </button>
              </>
            )}
          </div>
        </div>

        {/* Presets */}
        {timeLeft === totalTime && (
          <div className="glass rounded-xl p-6 mb-6">
            <h3 className="font-bold mb-4 text-center">Choose Duration</h3>
            
            <div className="mb-4">
              <p className="text-sm text-purple-300 mb-2">Work Session</p>
              <div className="flex gap-2 flex-wrap justify-center">
                {PRESETS.work.map((m) => (
                  <button
                    key={m}
                    onClick={() => handleStart(m, 'work')}
                    className="px-4 py-2 bg-purple-600 hover:bg-purple-700 rounded-lg"
                  >
                    {m} min
                  </button>
                ))}
              </div>
            </div>

            <div className="flex gap-4 justify-center">
              <div>
                <p className="text-sm text-purple-300 mb-2">Short Break</p>
                <div className="flex gap-2">
                  {PRESETS.short_break.map((m) => (
                    <button
                      key={m}
                      onClick={() => handleStart(m, 'short_break')}
                      className="px-4 py-2 bg-green-600 hover:bg-green-700 rounded-lg"
                    >
                      {m} min
                    </button>
                  ))}
                </div>
              </div>
              <div>
                <p className="text-sm text-purple-300 mb-2">Long Break</p>
                <div className="flex gap-2">
                  {PRESETS.long_break.map((m) => (
                    <button
                      key={m}
                      onClick={() => handleStart(m, 'long_break')}
                      className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg"
                    >
                      {m} min
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Sounds */}
        <div className="glass rounded-xl p-6 mb-6">
          <h3 className="font-bold mb-3">馃幍 Ambient Sounds</h3>
          <div className="flex gap-2 flex-wrap">
            {sounds.filter(s => !s.is_premium).map((s) => (
              <button
                key={s.id}
                onClick={() => setSelectedSound(selectedSound === s.name ? null : s.name)}
                className={`px-4 py-2 rounded-lg ${selectedSound === s.name ? 'bg-purple-600' : 'bg-white/10 hover:bg-white/20'}`}
              >
                {s.emoji} {s.name}
              </button>
            ))}
          </div>
        </div>

        {/* Achievements */}
        {achievements.length > 0 && (
          <div className="glass rounded-xl p-6">
            <h3 className="font-bold mb-3">馃弳 Recent Achievements</h3>
            <div className="flex gap-3 flex-wrap">
              {achievements.slice(0, 5).map((a, i) => (
                <div key={i} className="px-4 py-2 bg-white/10 rounded-lg text-center">
                  <span className="text-2xl">{a.icon}</span>
                  <p className="text-xs">{a.name}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Stats Modal */}
        {showStats && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4" onClick={() => setShowStats(false)}>
            <div className="glass rounded-xl p-6 max-w-md w-full" onClick={e => e.stopPropagation()}>
              <h2 className="text-xl font-bold mb-4">馃搳 Your Stats</h2>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span>Total Focus Time</span>
                  <span className="font-bold">{user?.total_focus_minutes || 0} min</span>
                </div>
                <div className="flex justify-between">
                  <span>Current Streak</span>
                  <span className="font-bold">馃敟 {user?.current_streak || 0} days</span>
                </div>
                <div className="flex justify-between">
                  <span>Longest Streak</span>
                  <span className="font-bold">{user?.longest_streak || 0} days</span>
                </div>
                <hr className="border-white/20" />
                <p className="text-sm text-purple-300 mb-2">Last 7 Days</p>
                <div className="flex gap-1 h-20 items-end">
                  {dailyStats.slice(0, 7).reverse().map((d, i) => (
                    <div key={i} className="flex-1 flex flex-col items-center">
                      <div 
                        className="w-full bg-purple-500 rounded-t"
                        style={{ height: `${Math.min(100, (d.focus_minutes / 120) * 100)}%` }}
                      />
                      <span className="text-xs mt-1">{d.focus_minutes}m</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}
