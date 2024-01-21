import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

export default function ResultTable(data: any) {
  return (
    <TableContainer component={Paper} sx={{margin: 5}}>
            <Table sx={{ minWidth: 650 }} size="small" aria-label="a dense table">
        <TableHead>
          <TableRow>
            <TableCell>index</TableCell>
            <TableCell>IO coefficient</TableCell>
            <TableCell>IO tau static</TableCell>
            <TableCell>AO coefficient</TableCell>
            <TableCell>AO tau static</TableCell>
            <TableCell>TC coefficient</TableCell>
            <TableCell>TC tau static</TableCell>
            <TableCell>LS coefficient</TableCell>
            <TableCell>LS tau static</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
                    {data.data.map((row: any) => (
            <TableRow
              key={row.index}
              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
            >
              <TableCell component="th" scope="row">
                {row.index}
              </TableCell>
              <TableCell align="right">{row.IOcoef}</TableCell>
              <TableCell align="right">{row.IOtstat}</TableCell>
              <TableCell align="right">{row.AOcoef}</TableCell>
              <TableCell align="right">{row.AOtstat}</TableCell>
              <TableCell align="right">{row.TCcoef}</TableCell>
              <TableCell align="right">{row.TCtstat}</TableCell>
              <TableCell align="right">{row.LScoef}</TableCell>
              <TableCell align="right">{row.LStstat}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
