import { render, screen, fireEvent } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { vi } from 'vitest'
import { App } from './App'

// Мокаем глобальные зависимости
vi.stubGlobal('fetch', vi.fn(() =>
  Promise.resolve({
    ok: true,
    blob: () => Promise.resolve(new Blob(['dummy data'], { type: 'image/jpeg' })),
  })
))

vi.stubGlobal('URL', {
  createObjectURL: vi.fn(() => 'blob:http://localhost/fake-url'),
  revokeObjectURL: vi.fn(),
})

describe('App', () => {
  afterEach(() => {
    vi.clearAllMocks()
  })

  it('отображает начальные элементы', () => {
    render(<App />)

    expect(screen.getByRole('button', { name: /Выбрать файл/i })).toBeInTheDocument()
  })

  it('отображает кнопки после выбора файла', async () => {
    render(<App />)

    const file = new File(['test content'], 'test.jpg', { type: 'image/jpeg' })
    const input = screen.getByTestId('file-input') 
    await userEvent.upload(input, file)

    expect(await screen.findByText(/Файл выбран/i)).toBeInTheDocument()

    expect(screen.getByRole('button', { name: /Обработать/i })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /Выбрать другой файл/i })).toBeInTheDocument()
  })

  it('обрабатывает файл при клике на "Обработать"', async () => {
    render(<App />)

    const file = new File(['test content'], 'test.jpg', { type: 'image/jpeg' })
    const hiddenInput = screen.getByTestId('file-input')
    await userEvent.upload(hiddenInput, file)

    const processButton = await screen.findByRole('button', { name: /Обработать/i })
    fireEvent.click(processButton)

    // Ждём кнопку скачивания с увеличенным таймаутом (3 секунды)
    const downloadButton = await screen.findByTestId('down-file', {}, { timeout: 3000 })
    expect(downloadButton).toBeInTheDocument()
  })

})
