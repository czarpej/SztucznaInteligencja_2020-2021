package slidingPuzzle;

import sac.State;
import sac.StateFunction;

public class ManhattanHeuristic extends StateFunction {
	@Override
	public double calculate(State state) {
		slidingPuzzle p = (slidingPuzzle) state;
		
		int k = 0, h = 0;
		
		for (int i = 0; i < p.n; i++) {
			for (int j = 0; j < p.n; j++, k++) {
				if(p.board[i][j] != k) {
					int i_new = p.board[i][j] / p.n, j_new = p.board[i][j] % p.n;
					h += Math.abs(i - i_new) + Math.abs(j - j_new);
				}
			}
		}
		
		return h;
	}
}
