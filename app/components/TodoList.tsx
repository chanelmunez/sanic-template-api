'use client'

import { useState } from 'react'
import axios from 'axios'

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

interface TodoListProps {
  todos: Todo[]
  users: User[]
  onTodoCreated: (todo: Todo) => void
  onTodosUpdated: (todos: Todo[]) => void
}

export default function TodoList({ todos, users, onTodoCreated, onTodosUpdated }: TodoListProps) {
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [selectedUserId, setSelectedUserId] = useState<number | ''>('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!title.trim() || !description.trim() || !selectedUserId) {
      setError('Please fill in all fields')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const response = await axios.post('/api/python/todos', {
        title: title.trim(),
        description: description.trim(),
        user_id: selectedUserId
      })
      
      onTodoCreated(response.data)
      setTitle('')
      setDescription('')
      setSelectedUserId('')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create todo')
    } finally {
      setLoading(false)
    }
  }

  const toggleTodo = async (todoId: number) => {
    try {
      const todo = todos.find(t => t.id === todoId)
      if (!todo) return

      await axios.put(`/api/python/todos/${todoId}`, {
        completed: !todo.completed
      })

      const updatedTodos = todos.map(t => 
        t.id === todoId ? { ...t, completed: !t.completed } : t
      )
      onTodosUpdated(updatedTodos)
    } catch (err) {
      console.error('Failed to update todo:', err)
    }
  }

  const getUserName = (userId: number) => {
    const user = users.find(u => u.id === userId)
    return user ? user.name : 'Unknown User'
  }

  return (
    <div>
      <form onSubmit={handleSubmit} className="space-y-4 mb-6">
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-3 py-2 rounded text-sm">
            {error}
          </div>
        )}
        
        <div>
          <label htmlFor="todo-title" className="block text-sm font-medium text-gray-700 mb-1">
            Title
          </label>
          <input
            type="text"
            id="todo-title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Enter todo title"
            disabled={loading}
          />
        </div>

        <div>
          <label htmlFor="todo-description" className="block text-sm font-medium text-gray-700 mb-1">
            Description
          </label>
          <textarea
            id="todo-description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={3}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Enter todo description"
            disabled={loading}
          />
        </div>

        <div>
          <label htmlFor="user-select" className="block text-sm font-medium text-gray-700 mb-1">
            Assign to User
          </label>
          <select
            id="user-select"
            value={selectedUserId}
            onChange={(e) => setSelectedUserId(e.target.value ? Number(e.target.value) : '')}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            disabled={loading}
          >
            <option value="">Select a user</option>
            {users.map((user) => (
              <option key={user.id} value={user.id}>
                {user.name}
              </option>
            ))}
          </select>
        </div>

        <button
          type="submit"
          disabled={loading || users.length === 0}
          className="w-full bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'Creating...' : 'Create Todo'}
        </button>
      </form>

      <div>
        <h3 className="text-lg font-semibold text-gray-700 mb-4">
          Todos ({todos.length})
        </h3>
        <div className="space-y-3">
          {todos.map((todo) => (
            <div key={todo.id} className="bg-gray-50 p-4 rounded-lg">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className={`font-medium ${todo.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                    {todo.title}
                  </div>
                  <div className={`text-sm mt-1 ${todo.completed ? 'text-gray-400' : 'text-gray-600'}`}>
                    {todo.description}
                  </div>
                  <div className="text-xs text-gray-500 mt-2 flex items-center space-x-4">
                    <span>Assigned to: {getUserName(todo.user_id)}</span>
                    <span>Created: {new Date(todo.created_at).toLocaleDateString()}</span>
                  </div>
                </div>
                <button
                  onClick={() => toggleTodo(todo.id)}
                  className={`ml-4 px-3 py-1 rounded text-sm font-medium ${
                    todo.completed
                      ? 'bg-yellow-100 text-yellow-800 hover:bg-yellow-200'
                      : 'bg-green-100 text-green-800 hover:bg-green-200'
                  }`}
                >
                  {todo.completed ? 'Undo' : 'Complete'}
                </button>
              </div>
            </div>
          ))}
          {todos.length === 0 && (
            <div className="text-gray-500 text-center py-8">
              No todos yet. Create one above!
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
