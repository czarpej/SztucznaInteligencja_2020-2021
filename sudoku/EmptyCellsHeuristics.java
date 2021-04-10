package sudoku;

import sac.State;
import sac.StateFunction;

public class EmptyCellsHeuristics extends StateFunction {
	@Override
	public double calculate(State state) {
		Sudoku sudoku = (Sudoku) state;
		return sudoku.getZeros();
	}
}
