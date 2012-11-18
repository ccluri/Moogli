#-------------------------------------------------------------------------------
# Script params
#-------------------------------------------------------------------------------

# Number of cell copies to create.
n_copies = 2

infile = 'ca1_absolute.p'
outfile = 'ca1.csv'
moniker = 'ca1'

# Files to pick time-series data from.
time_series_files = (
	'calcium.plot',
	'mRNA.plot',
)

# Names of the variables being displayed.
field_names = (
	'Ca',
	'mRNA',
)

# Specifies translation of each cell through space.
shift = (
	( -200, -800, 0 ),
	( 200, -800, 0 ),
)

# Scale diameter of compartments, for easier viewing.
dia_scale = 12.0

#-------------------------------------------------------------------------------
# Handling time-series data.
#-------------------------------------------------------------------------------
def read_xplot( xfile ):
	with open( xfile, 'r' ) as fin:
		dat = fin.read()
	dat = dat.split( '\n' )
	
	series = {}
	min_value = float( 'Inf' )
	max_length = 0
	
	for line in dat:
		line = line.strip()
		
		if not line or line == '/newplot':
			if len( series ) > 0:
				if len( y ) > max_length:
					max_length = len( y )
				if min( y ) < min_value:
					min_value = min( y )
			
			continue
		
		if line[ :9 ] == '/plotname':
			compt = line.split( ' ' )[ 1 ]
			series[ compt ] = []
			y = series[ compt ]
		else:
			try:
				value = float( line )
			except ValueError:
				raise( "Oops! Looks like the line '{0}' in file {1} is either "
				       "not a number, or has come before "
				       "any '/plotname'.".format( line, xfile ) )
			
			y.append( value )
	
	return ( series, min_value, max_length )

time_series = []
n_frames = 0
min_values = []
for tfile in time_series_files:
	( y, min_value, max_length ) = read_xplot( tfile )
	
	time_series.append( y )
	min_values.append( min_value )
	if max_length > n_frames:
		n_frames = max_length

for ( y, min_value ) in zip( time_series, min_values ):
	for values in y.values():
		padding_size = n_frames - len( values )
		padding = ( min_value, ) * padding_size
		values.extend( padding )
	
	y[ None ] = ( min_value, ) * n_frames

#-------------------------------------------------------------------------------
# Reading cells, munging, writing.
#-------------------------------------------------------------------------------

with open( infile, 'r' ) as fin:
	dat = fin.read()

dat = dat.split( '\n' )
dat = [ i.split( '\t' ) for i in dat if i and i[ 0 ] != '*' ]

class Compartment:
	def __init__( self, p0, p1, dia ):
		self.p0 = p0
		self.p1 = p1
		self.dia = dia

def process( dat, shift ):
	'''Takes data read from file, and returns it in a more useful
	format. For example, finds out coordinates of parent compartments.
	
	Also shifts cell through space, and scales diameter.
	'''
	store = {}
	
	for ( compt, parent, x1, y1, z1, dia ) in dat:
		if parent == 'none':
			p0 = shift
		else:
			if parent == '.':
				parent = previous
			p0 = store[ parent ].p1
		
		p1 = [ float( i ) for i in ( x1, y1, z1 ) ]
		
		# Translating through space.
		for i in range( 3 ):
			p1[ i ] += shift[ i ]
		
		# Scaling diameter.
		dia = dia_scale * float( dia )
		
		store[ compt ] = Compartment( p0, p1, dia )
		
		previous = compt
	
	return store

def dump( writer, cell_index, dat, store, y, field_name ):
	'''Writes data to file: 1 cell per call.'''
	
	cell_moniker = moniker + '_' + str( cell_index )
	
	for record in dat:
		compt = record[ 0 ]
		cc = store[ compt ]
		
		( ( x0, y0, z0 ), ( x1, y1, z1 ), dia ) = ( cc.p0, cc.p1, cc.dia )
		
		row = [ cell_moniker, compt, x0, y0, z0, x1, y1, z1, dia, field_name ]
		
		if compt in y:
			values = y[ compt ]
		else:
			values = y[ None ]
		
		row.extend( values )
		
		writer.writerow( row )

import csv
csv.register_dialect( 'tab', delimiter = '\t' )
with open( outfile, 'w' ) as fout:
	writer = csv.writer( fout, 'tab' )
	
	for ii in range( n_copies ):
		store = process( dat, shift[ ii ] )
		dump( writer, ii, dat, store, time_series[ ii ], field_names[ ii ] )
