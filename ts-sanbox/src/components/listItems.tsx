import * as React from 'react';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import HomeTwoToneIcon from '@mui/icons-material/HomeTwoTone';
import SsidChartTwoToneIcon from '@mui/icons-material/SsidChartTwoTone';
import StackedLineChartTwoToneIcon from '@mui/icons-material/StackedLineChartTwoTone';
import ScheduleTwoToneIcon from '@mui/icons-material/ScheduleTwoTone';

export const mainListItems = (
    <>
        <ListItemButton href="/">
            <ListItemIcon>
                <HomeTwoToneIcon />
            </ListItemIcon>
            <ListItemText primary="Home" />
        </ListItemButton>
        <ListItemButton href="/analyze">
            <ListItemIcon>
                <SsidChartTwoToneIcon />
            </ListItemIcon>
            <ListItemText primary="Analyze" />
        </ListItemButton>
        <ListItemButton href='/effects'>
            <ListItemIcon>
                <StackedLineChartTwoToneIcon />
            </ListItemIcon>
            <ListItemText primary="Effects" />
        </ListItemButton>
        <ListItemButton href='/history'>
            <ListItemIcon>
                <ScheduleTwoToneIcon />
            </ListItemIcon>
            <ListItemText primary="History" />
        </ListItemButton>
    </>
);

