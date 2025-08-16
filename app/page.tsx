'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'
import TodoList from './components/TodoList'
import UserForm from './components/UserForm'

interface User {
  id: number
  name: string
  email: string
  created_at: string
}

interface Todo {
  id: number
  title: string
  description: string
  completed: boolean
  user_id: number
  created_at: string
}

export default function Home() {
  const [users, setUsers] = useState<User[]>([])
  const [todos, setTodos] = useState<Todo[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchData = async () => {
    try {
      setLoading(true)
      const [usersRes, todosRes] = await Promise.all([
        axios.get('/api/python/users'),
        axios.get('/api/python/todos')
      ])
      setUsers(usersRes.data)
      setTodos(todosRes.data)
      setError(null)
    } catch (err) {
      setError('Failed to fetch data from API')
      console.error('API Error:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
  }, [])

  const handleUserCreated = (newUser: User) => {
    setUsers([...users, newUser])
  }

  const handleTodoCreated = (newTodo: Todo) => {
    setTodos([...todos, newTodo])
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-xl font-semibold text-gray-700">Loading...</div>
      </div>
    )
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Sanic + Next.js Template
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            A full-stack template showcasing Next.js TypeScript frontend with Sanic Python backend,
            designed for Vercel serverless deployment.
          </p>
        </div>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-8">
            <strong>Error:</strong> {error}
            <button 
              onClick={fetchData}
              className="ml-4 bg-red-500 text-white px-3 py-1 rounded text-sm hover:bg-red-600"
            >
              Retry
            </button>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">Users Management</h2>
            <UserForm onUserCreated={handleUserCreated} />
            
            <div className="mt-8">
              <h3 className="text-lg font-semibold text-gray-700 mb-4">
                Users ({users.length})
              </h3>
              <div className="space-y-3">
                {users.map((user) => (
                  <div key={user.id} className="bg-gray-50 p-4 rounded-lg">
                    <div className="font-medium text-gray-900">{user.name}</div>
                    <div className="text-sm text-gray-600">{user.email}</div>
                    <div className="text-xs text-gray-500 mt-1">
                      Created: {new Date(user.created_at).toLocaleDateString()}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">Todo Management</h2>
            <TodoList 
              todos={todos} 
              users={users}
              onTodoCreated={handleTodoCreated}
              onTodosUpdated={setTodos}
            />
          </div>
        </div>

        <div className="mt-12 bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">API Status</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <div className="font-semibold text-green-800">Backend Status</div>
              <div className="text-sm text-green-600">Sanic API Connected</div>
            </div>
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <div className="font-semibold text-blue-800">Frontend</div>
              <div className="text-sm text-blue-600">Next.js App Router</div>
            </div>
            <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
              <div className="font-semibold text-purple-800">Deployment</div>
              <div className="text-sm text-purple-600">Vercel Ready</div>
            </div>
          </div>
        </div>
      </div>
    </main>
  )
}
