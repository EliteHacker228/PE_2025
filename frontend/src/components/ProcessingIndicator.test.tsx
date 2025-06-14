import { render, screen } from '@testing-library/react'
import { ProcessingIndicator } from './ProcessingIndicator'

describe('ProcessingIndicator', () => {
  it('отображает индикатор и текст обработки', () => {
    render(<ProcessingIndicator />)

    expect(screen.getByText(/идёт обработка файла/i)).toBeInTheDocument()
    expect(document.querySelector('.loader')).toBeInTheDocument()
  })
})
