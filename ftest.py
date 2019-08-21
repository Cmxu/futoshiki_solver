import numpy as np
from itertools import permutations, chain, combinations
import sys
from contextlib import suppress

N = 0

known_board = []
completed_squares = []
ineq = []

if len(sys.argv) == 1:
	print('UNFINISHED: Manual Entry (Please Provide File)')
	
#	for i in range(N):
#		print('Row ' + str(i + 1) + ': ', end = '')
#		inp = input()
#		inp = np.asarray([int(i) for i in list(inp)])
#		known_board[i] = inp
#		for j in range(N):
#			if inp[j] != 0:
#				completed_squares[i][j] = True
else:
	file_name = sys.argv[1]
	with open(file_name, 'r') as file:
		for line in file:
			N = int(len(line)/2)
			known_board = np.zeros((N,N), dtype = 'int')
			completed_squares = [[False for i in range(N)] for j in range(N)]
			ineq = []
			break
	with open(file_name, 'r') as file:
		i = 0
		for line in file:
			if i % 2 == 0:
				#inp = np.asarray([int(i) for i in list(line[:-1])])
				inp = np.asarray([int(a) for a in [line[2*b] for b in range(N)]])
				known_board[int(i/2)] = inp
				for j in range(N):
					if inp[j] != 0:
						completed_squares[int(i/2)][j] = True
				for j in range(len(line)):
					if line[j] == '>':
						ineq.append([[int(i/2),int((j-1)/2)],[int(i/2),int((j+1)/2)]])
					elif line[j] == '<':
						ineq.append([[int(i/2),int((j+1)/2)],[int(i/2),int((j-1)/2)]])
			else:
				for j in range(len(line)):
					if line[j] == 'v':
						ineq.append([[int((i-1)/2),int(j/2)],[int((i+1)/2),int(j/2)]])
					elif line[j] == '^':	
						ineq.append([[int((i+1)/2),int(j/2)],[int((i-1)/2),int(j/2)]])
			i += 1

def add(x, y, n):
	known_board[x][y] = n
	completed_squares[x][y] = True

def poss():
	parr = [[[i+1 for i in range(N)] for j in range(N)] for k in range(N)]
	for i in range(N):
		for j in range(N):
			if known_board[i][j] != 0:
				for k in range(N):
					with suppress(ValueError, AttributeError):
						parr[i][k].remove(known_board[i][j])
					with suppress(ValueError, AttributeError):
						parr[k][j].remove(known_board[i][j])
				parr[i][j] = [known_board[i][j]]
	return parr

def pr_arr(arr):
	for i in range(N):
		print(*[[str(i) if i in a else '_' for i in range(1,N+1)] for a in arr[i]], sep = '\t')

def pr_brd(nd = -1):
	for i in range(N):
		if nd == -1:
			print(''.join([str(a) if a != 0 else '-' for a in known_board[i]]))
		elif i == int(N/2):	
			print(str(nd) + '\t' + ''.join([str(a) if a != 0 else '-' for a in known_board[i]]))
		else:
			print('\t' + ''.join([str(a) if a != 0 else '-' for a in known_board[i]]))
def sol_ineq(ps):
	ps = np.asarray(ps)
	for inq in ineq:
		big = tuple(inq[0])
		sml = tuple(inq[1])
		while min(ps[big]) <= min(ps[sml]):
			ps[big].remove(min(ps[big]))
		while max(ps[sml]) >= max(ps[big]):
			ps[sml].remove(max(ps[sml]))
	return ps


def sol_al(ps):
	for i in range(N):
		count = [[] for _ in range(N)]
		for j in range(N):
			for k in ps[i][j]:
				count[int(k - 1)].append(j)
		for j in range(N):	
			if len(count[j]) == 1:
				ps[i][count[j][0]] = list([j+1])
	for i in range(N):
		count = [[] for _ in range(N)]
		for j in range(N):
			for k in ps[j][i]:
				count[int(k-1)].append(j)
		for j in range(N):
			if len(count[j]) == 1:
				ps[count[j][0]][i] = list([j+1])
	return ps

def find_al(ps):
	for i in range(N):
		for j in range(N):
			if len(ps[i][j]) == 1:
				if not completed_squares[i][j]:
					add(i,j,ps[i][j][0])

def find_sub(ps):
	sub_rows = []
	ps = np.asarray(ps)
	for i in range(N):
		uns = []
		for j in range(N):
			if len(ps[i][j]) > 1:
				uns.append(j)
		for j in range(2, len(uns) - 1):
			for comb in combinations(uns, j):
				bo = set(chain.from_iterable(ps[i, comb]))
				if len(bo) <= j:
					sub_rows.append([i, comb, bo])
	sub_cols = []
	for i in range(N):
		uns = []
		for j in range(N):
			if len(ps[j][i]) > 1:
				uns.append(j)
		for j in range(2, len(uns) - 1):
			for comb in combinations(uns, j):
				bo = set(chain.from_iterable(ps[comb, i]))
				if len(bo) <= j:
					sub_cols.append([i, comb, bo])
	return sub_rows, sub_cols

def sol_sub(ps, sub_rows, sub_cols):
	for i, comb, bo in sub_rows:
		for j in range(N):
			if j not in comb:
				for k in bo:
					with suppress(ValueError, AttributeError):
						ps[i][j].remove(k)
	for i, comb, bo in sub_cols:
		for j in range(N):
			if j not in comb:
				for k in bo:
					with suppress(ValueError, AttributeError):
						ps[j][i].remove(k)
	return ps 

def ssub(ps):
	sub_rows, sub_cols = find_sub(ps)
	return sol_sub(ps, sub_rows, sub_cols)

def solve(verbose = False):
	done = np.sum(np.asarray(completed_squares))
	if verbose:
		print('='*(len('\t'.expandtabs())+N))
		pr_brd(done)
		print('='*(len('\t'.expandtabs())+N))
	stal_count = 0
	while done != N*N:
		ps = poss()
		ps = sol_ineq(ps)
		ps = sol_al(ps)
		find_al(ps)
		nd = np.sum(np.asarray(completed_squares))
		#print(nd)
		if done == nd:
			stal_count += 1
			if stal_count >= 10:
				print('I seem to be stuck... did you miss something? (or do I need a new algorithm)')
				break
			ssub(ps)
			ps = sol_ineq(ps)
			ps = sol_al(ps)
			find_al(ps)
			nd = np.sum(np.asarray(completed_squares))
			if verbose:
				pr_brd(nd)
				print('='*(len('\t'.expandtabs())+N))
		else:
			stal_count = 0
			if verbose:
				pr_brd(nd)
				print('='*(len('\t'.expandtabs())+N))
			done = nd
