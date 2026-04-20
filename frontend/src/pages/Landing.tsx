import { Link } from 'react-router-dom'

export default function Landing() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4">
      <div className="text-center mb-8">
        <div className="text-7xl mb-4 animate-pulse-ring">鈴憋笍</div>
        <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-pink-400 to-purple-400 bg-clip-text text-transparent mb-2">
          FocusFlow
        </h1>
        <p className="text-xl text-purple-200">Gamified Pomodoro Timer</p>
      </div>

      <div className="grid md:grid-cols-3 gap-6 mb-8 max-w-3xl">
        <div className="glass rounded-xl p-6 text-center">
          <div className="text-4xl mb-2">馃崊</div>
          <h3 className="font-bold mb-1">Pomodoro Timer</h3>
          <p className="text-sm text-purple-200">25/5 minute cycles for optimal focus</p>
        </div>
        <div className="glass rounded-xl p-6 text-center">
          <div className="text-4xl mb-2">馃幍</div>
          <h3 className="font-bold mb-1">Ambient Sounds</h3>
          <p className="text-sm text-purple-200">Rain, caf茅, forest & more</p>
        </div>
        <div className="glass rounded-xl p-6 text-center">
          <div className="text-4xl mb-2">馃弳</div>
          <h3 className="font-bold mb-1">Achievements</h3>
          <p className="text-sm text-purple-200">Unlock badges, earn coins</p>
        </div>
      </div>

      <div className="flex gap-4">
        <Link to="/login" className="px-8 py-3 bg-purple-600 hover:bg-purple-700 rounded-lg font-semibold transition">
          Login
        </Link>
        <Link to="/register" className="px-8 py-3 bg-pink-600 hover:bg-pink-700 rounded-lg font-semibold transition">
          Get Started
        </Link>
      </div>
    </div>
  )
}
