/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   asm.c                                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: bwan-nan <bwan-nan@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/07/25 13:44:04 by bwan-nan          #+#    #+#             */
/*   Updated: 2019/07/25 15:20:51 by bwan-nan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "asm.h"

static int		print_usage(void)
{
	ft_putendl("Usage: ./asm <sourcefile.s>");
	return (1);
}

static void		init_asm(t_asm *glob)
{
	glob->input = NULL;
	glob->labels = NULL;
	glob->current_label = NULL;
	glob->param = 0;
	glob->ptr = NULL;
	glob->ocp_ptr = NULL;
	glob->queue = NULL;
	glob->byte_nbr = 0;
	glob->inst_count = 0;
	glob->name_length = 0;
	glob->comment_length = 0;
}

int				print_error(char *msg, int line_number)
{
	if (!line_number)
		ft_putendl(msg);
	else
		ft_printf("%s in line %d.\n", msg, line_number);
	return (0);
}

int				main(int ac, char **av)
{
	t_asm	glob;

	init_asm(&glob);
	if (ac != 2 || !file_exists(av[1]))
		return (print_usage());
	if (!get_input(&glob.input, av[1]))
		return (-1); // free input, si ret == 0, print "ERROR", si =-1 print "lexical_error" Free_input(&glob.input)
	if (!lexer(&glob))
		return (-1); // free input
	reorder_list(&glob.input);
	return (create_cor_file(&glob, av[1]) != -1);
}
