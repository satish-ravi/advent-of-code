input = IO.read(:stdio, :eof)

defmodule Solution do

    def parse(input) do
      input |> String.graphemes() |> Enum.map(&String.to_integer/1)
    end

    def sum_matches(nums, offset) do
        shifted = Enum.drop(nums, offset) ++ Enum.take(nums, offset)

        nums
        |> Enum.zip(shifted)
        |> Enum.filter(fn {a, b} -> a == b end)
        |> Enum.map(fn {a, _} -> a end)
        |> Enum.sum()
    end

    def part1(nums) do
        sum_matches(nums, 1)
    end

    def part2(nums) do
        sum_matches(nums, div(length(nums), 2))
    end
end

nums = Solution.parse(input)
IO.puts("Part 1: #{Solution.part1(nums)}")
IO.puts("Part 2: #{Solution.part2(nums)}")
