package main

import (
	"fmt"
	"math/big"
	"os"
	"sort"
	"strconv"
	"strings"
)

func splitOnNewline(lines []string) [][]string {
	blocks := make([][]string, 1)
	for _, line := range lines {
		if line == "" {
			blocks = append(blocks, nil)
		} else {
			blocks[len(blocks)-1] = append(blocks[len(blocks)-1], line)
		}
	}
	if len(blocks[len(blocks)-1]) == 0 {
		return blocks[:len(blocks)-1]
	}
	return blocks
}

type monkey struct {
	items          []*big.Int
	op             func(*big.Int) *big.Int
	divisibleTest  *big.Int
	throwTrue      int
	throwFalse     int
	inspectedCount uint64
}

func check2[T any](v T, err error) T {
	if err != nil {
		panic(err)
	}
	return v
}

func lastInt(s string) int {
	f := strings.Fields(s)
	return check2(strconv.Atoi(f[len(f)-1]))
}

func lastBig(s string) *big.Int {
	f := strings.Fields(s)
	return big.NewInt(check2(strconv.ParseInt(f[len(f)-1], 10, 64)))
}

func parseItems(s string) []*big.Int {
	itemsRaw := strings.Split(strings.TrimSpace(strings.Split(s, ":")[1]), ", ")
	items := make([]*big.Int, len(itemsRaw))
	for i, itemRaw := range itemsRaw {
		items[i] = big.NewInt(check2(strconv.ParseInt(itemRaw, 10, 64)))
	}
	return items
}

func parseOp(s string) func(*big.Int) *big.Int {
	opRaw := strings.Fields(s)
	switch opRaw[len(opRaw)-2] {
	case "+":
		y := lastBig(opRaw[len(opRaw)-1])
		return func(old *big.Int) *big.Int {
			var z big.Int
			return z.Add(old, y)
		}
	case "*":
		if opRaw[len(opRaw)-1] == "old" {
			return func(old *big.Int) *big.Int {
				var z big.Int
				return z.Mul(old, old)
			}
		}
		y := lastBig(opRaw[len(opRaw)-1])
		return func(old *big.Int) *big.Int {
			var z big.Int
			return z.Mul(old, y)
		}
	default:
		panic("internal")
	}
}

func parse(monkeysRaw [][]string) []*monkey {
	monkeys := make([]*monkey, 0)
	for _, monkeyRaw := range monkeysRaw {
		monkeys = append(monkeys, &monkey{
			items:         parseItems(monkeyRaw[1]),
			op:            parseOp(monkeyRaw[2]),
			divisibleTest: lastBig(monkeyRaw[3]),
			throwTrue:     lastInt(monkeyRaw[4]),
			throwFalse:    lastInt(monkeyRaw[5]),
		})
	}
	return monkeys
}

var three = big.NewInt(3)

func round(monkeys []*monkey, decreaseWorryLevel bool) {
	for _, monkey := range monkeys {
		for _, item := range monkey.items {
			newWorryLevel := monkey.op(item)
			if decreaseWorryLevel {
				newWorryLevel.Div(newWorryLevel, three)
			}
			var z big.Int
			if z.Mod(newWorryLevel, monkey.divisibleTest).Sign() == 0 {
				nextItems := &monkeys[monkey.throwTrue].items
				*nextItems = append(*nextItems, newWorryLevel)
			} else {
				nextItems := &monkeys[monkey.throwFalse].items
				*nextItems = append(*nextItems, newWorryLevel)
			}
		}

		monkey.inspectedCount += uint64(len(monkey.items))
		monkey.items = monkey.items[:0]
	}
}

func monkeyBusiness(monkeys []*monkey, rounds int, decreaseWorryLevel bool) uint64 {
	for i := 0; i < rounds; i++ {
		round(monkeys, decreaseWorryLevel)
	}
	sort.Slice(monkeys, func(i, j int) bool {
		return monkeys[i].inspectedCount > monkeys[j].inspectedCount
	})
	return monkeys[0].inspectedCount * monkeys[1].inspectedCount
}

func main() {
	monkeysRawConcat := string(check2(os.ReadFile("input_test.txt")))
	monkeysRawLines := strings.Split(strings.TrimSpace(monkeysRawConcat), "\n")
	monkeysRaw := splitOnNewline(monkeysRawLines)
	fmt.Println(monkeyBusiness(parse(monkeysRaw), 20, true))
	fmt.Println(monkeyBusiness(parse(monkeysRaw), 800, false))
}
