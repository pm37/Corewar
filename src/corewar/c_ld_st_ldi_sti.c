/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   c_ld_st_ldi_sti.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jboursal <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/07/17 14:37:54 by jboursal          #+#    #+#             */
/*   Updated: 2019/07/30 16:51:19 by fdagbert         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "corewar.h"

int		c_ld(t_process *process, t_conf *conf)
{
	int		index;
	int		reg1;
	int		pc;

	index = process->fct_args[0];
	reg1 = process->fct_args[1];
	pc = process->pc;
	if (process->ocp_splitted.arg2 != REG_CODE
			|| reg1 <= 0 || reg1 > REG_NUMBER)
		return (1);
	if (process->ocp_splitted.arg1 == IND_CODE)
		process->reg[reg1 - 1] = c_modulo_indirect(1, pc, index, conf);
	else if (process->ocp_splitted.arg1 == DIR_CODE)
		process->reg[reg1 - 1] = index;
	else
		return (1);
	process->carry = 0;
	if (!index)
		process->carry = 1;
	return (1);
}

int		c_st(t_process *process, t_conf *conf)
{
	int		reg1;
	int		index;
	int		pc;

	reg1 = process->fct_args[0];
	index = process->fct_args[1];
	pc = process->pc;
	if (process->ocp_splitted.arg1 != REG_CODE
			|| reg1 <= 0 || reg1 > REG_NUMBER)
		return (1);
	if (process->ocp_splitted.arg2 == IND_CODE)
	{
		pc = c_modulo_indirect(0, pc, index, conf);
		conf->grid[pc]->val = process->reg[reg1 - 1];
		conf->grid[pc]->pid = process->id_champ;
	}
	else if (process->ocp_splitted.arg2 == REG_CODE)
	{
		if (index > 0 && index <= REG_NUMBER)
			process->reg[index - 1] = process->reg[reg1 - 1];
	}
	return (1);
}

int		c_ldi(t_process *process, t_conf *conf)
{
	int		index1;
	int		index2;
	int		reg3;
	int		pc;
	int		sum;

	index1 = process->fct_args[0];
	index2 = process->fct_args[1];
	reg3 = process->fct_args[2];
	pc = process->pc;
	sum = 0;
	if (c_check_arg_type(index1, index2, reg3, process) == 1)
		return (1);
	if (process->ocp_splitted.arg1 == REG_CODE)
		index1 = process->reg[index1 - 1];
	else if (process->ocp_splitted.arg1 == IND_CODE)
		index1 = c_modulo_indirect(1, pc, index1, conf);
	if (process->ocp_splitted.arg2 == REG_CODE)
		index2 = process->reg[index2 - 1];
	else if (process->ocp_splitted.arg2 == IND_CODE)
		return (1);
	sum = c_sum(index1, index2, process);
	process->reg[reg3 - 1] = conf->grid[sum]->val;
	process->carry = 0;
	return (1);
}

int		c_sti(t_process *process, t_conf *conf)
{
	int		reg1;
	int		index2;
	int		index3;
	int		pc;
	int		sum;

	reg1 = process->fct_args[0];
	index2 = process->fct_args[1];
	index3 = process->fct_args[2];
	pc = process->pc;
	if (c_check_arg_type(index2, index3, reg1, process) == 1)
		return (1);
	if (process->ocp_splitted.arg2 == REG_CODE)
		index2 = process->reg[index2 - 1];
	else if (process->ocp_splitted.arg2 == IND_CODE)
		index2 = c_modulo_indirect(1, pc, index2, conf);
	if (process->ocp_splitted.arg3 == REG_CODE)
		index3 = process->reg[index3 - 1];
	else if (process->ocp_splitted.arg3 == IND_CODE)
		return (1);
	sum = c_sum(index2, index3, process);
	conf->grid[sum]->val = process->reg[reg1 - 1];
	conf->grid[sum]->pid = process->id_champ;
	process->carry = 0;
	return (1);
}