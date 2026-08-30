input = IO.read(:stdio, :eof)

defmodule Solution do

    def parse(input) do
        input
        |> String.trim()
        |> String.split("\n")
        |> Enum.map(fn line -> line |> String.split() |> Enum.map(&String.to_integer/1) end)
    end

    def part1(lines) do
        lines |> Enum.map(fn nums -> Enum.max(nums) - Enum.min(nums) end) |> Enum.sum()
    end

    def part2(lines) do
        lines
        |> Enum.map(fn nums ->
            Enum.find_value(Enum.with_index(nums), fn {a, i} ->
                Enum.find_value(Enum.with_index(nums), fn {b, j} ->
                    if i < j and rem(max(a, b), min(a, b)) == 0 do
                        div(max(a, b), min(a, b))
                    end
                end)
            end)
        end)
        |> Enum.sum()
    end
end

lines = Solution.parse(input)
IO.puts("Part 1: #{Solution.part1(lines)}")
IO.puts("Part 2: #{Solution.part2(lines)}")
