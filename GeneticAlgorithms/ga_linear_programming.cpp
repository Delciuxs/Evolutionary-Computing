//Version final, minimizando y maximizando eligiendo el individuo dominante a partir de Z
//codigo limpio

#include <bits/stdc++.h>
using namespace std;

//---------------------------------------------------------------------------------------------------------------------------------
//Estructura que almacenara todos los elementos necesarios de una variable: Sus limites inferior y superior, el numero de bits (m)
struct variable
{
	int m;
	double inferior, superior;
};
//---------------------------------------------------------------------------------------------------------------------------------
// Estructura que almacena los coeficientes de una restriccion(de todas las variables), el signo de la desigualdad ( >= o <= ) y el valor
// al cual se va a hacer la comparacion.
struct restriccion
{
	vector<double> coef;
	int signo;// signo 1 -> >= o 0 -> <=
	double igual;
};
//---------------------------------------------------------------------------------------------------------------------------------
//Funcion que nos retorna verdadero en el caso de que los valores de las variables de un individuo cumplan con todas las restricciones
bool se_puede_tomar_individuo(vector<double> valores_variables, vector<restriccion> restricciones, int num_var)
{
	double resul = 0.0;
	bool flag = false;

	for(int r = 0; r < restricciones.size(); r++)
	{
		resul = 0.0;

		//Evaluar la restriccion con los valores de las variables
		for(int v = 0; v < num_var; v++)
			resul += valores_variables[v] * restricciones[r].coef[v];

		if(restricciones[r].signo == 1)// La restriccion es del tipo >=
		{
			if(resul >= restricciones[r].igual)
				flag = true;
			else
			{
				flag = false;
				break;
			}
		}

		else// La restriccion es del tipo <=
		{
			if(resul <= restricciones[r].igual)
				flag = true;
			else
			{
				flag = false;
				break;
			}
		}
	}
	return flag;
}
//---------------------------------------------------------------------------------------------------------------------------------
//Funcion que genera solamente los valores v_j de cada variable apartir de la formula vista en clase y los almacena en una tabla
void genera_variables_j(int id_individuo, vector<int> random_var, vector<vector<double> > &individuos_variable_j, int num_var, unordered_map<char,variable> vars)
{
	double res = 0.0;
	char c = 'a';
	
	for(int v = 0; v < num_var; v++, c++)
	{
		res = vars[c].inferior + (random_var[v] * ((vars[c].superior - vars[c].inferior) / (pow(2, vars[c].m) - 1)));
		individuos_variable_j[id_individuo][v] = res;
	}
}
//---------------------------------------------------------------------------------------------------------------------------------
//Funcion que genera valores aleatorios para cada variable (por primera vez), en esta misma funcion se generan los valores v_j para los aleatorios generados
//de la misma forma se verifica que dichos valores v_j cumplan con todas las condiciones, de no ser así se crean nuevos valores aleatorios para las variables
void genera_aleatorios_variables(vector<vector<int> > &random_individuos, int num_individuos, unordered_map<char,variable> vars, int num_var, vector<vector<double> > &individuos_variable_j, vector<restriccion> restricciones)
{
	int aletario_maximo, num_random, i = 0;

	while(i < num_individuos)
	{
		char c = 'a';

		for(int j = 0; j < num_var; j++, c++)
		{
			aletario_maximo = pow(2, vars[c].m);//hasta que maximo aleatorio se puede generar a partir de los bits de precision
			num_random = rand() % aletario_maximo;
			random_individuos[i][j] = num_random;
		}

		genera_variables_j(i, random_individuos[i], individuos_variable_j, num_var, vars);

		if(se_puede_tomar_individuo(individuos_variable_j[i], restricciones, num_var))//pasa a generar el siguiente individuo
			i++;
	}
}
//---------------------------------------------------------------------------------------------------------------------------------
//Funcion que completa toda la matriz solucion, 1) evalua los valores de las v_j en la funcion objetivo Z
// 2) obtiene la P(z), 3) P(z) acumulada y 4) aleatorio entre 0 y 1 de 5 decimales
void completa_matriz(vector<vector<double> > &individuos_variable_j, int num_individuos, int num_var, vector<double> coeficientes_funcion)
{
	double z = 0.0, acumulado_z = 0.0;
	double aleat_0_1 = 0.0, num_aleat_0_1000 = 0.0;

	for(int i = 0; i < num_individuos; i++)
	{
		z = 0.0;
		for(int j = 0; j < num_var; j++)
			z += individuos_variable_j[i][j] * coeficientes_funcion[j];

		individuos_variable_j[i][num_var] = z;		
		acumulado_z += z;
	}

	double prob_z = 0.0;	
	double prob_z_acumul = 0.0;

	for(int i = 0; i < num_individuos; i++)
	{
		prob_z = individuos_variable_j[i][num_var] / acumulado_z;
		prob_z_acumul += prob_z;		
		individuos_variable_j[i][num_var + 1] = prob_z;
		individuos_variable_j[i][num_var + 2] = prob_z_acumul;
	}

	for(int i = 0; i < num_individuos; i++)
	{
		num_aleat_0_1000 = rand() % 10001;
		aleat_0_1 = num_aleat_0_1000 / 10000.0;
		individuos_variable_j[i][num_var + 3] = aleat_0_1;
	}
}
//---------------------------------------------------------------------------------------------------------------------------------
//Funcion que obtiene los individuos sobrevivientes, estos se obtienen a partir de ver en que rango cae el aleatorio de 0 a 1
//estos individuos permaneceran en la siguiente generacion de individuos, los demas se generarán a apartir de un individuo dominante
//este se obtiene a partir de la mayor/menor z segun se maximice o se minimice, para así tener individuos que se parezcan al dominante
int individuo_dominante, num_sobrevivientes;

unordered_map<int, int> individuos_sobrevivientes(vector<vector<double> > individuos_variable_j, int num_individuos, int num_var, bool max_min)
{
	individuo_dominante = 0, num_sobrevivientes = 0;
	double aleat_0_1 = 0.0;
	unordered_map<int, int> sobrevivientes;
	int id_individuo = 0;
	double mayor_z = -1.0;
	double menor_z = 1000000.0;

	for(int i = 0; i < num_individuos; i++)
	{
		id_individuo = 0;
		aleat_0_1 = individuos_variable_j[i][num_var + 3];

		if(max_min == true)//si estamos maximizando el dominante es el que tenga mayor Z
		{
			if(individuos_variable_j[i][num_var] > mayor_z)
			{
				mayor_z = individuos_variable_j[i][num_var];
				individuo_dominante = i;
			}
		}

		if(max_min == false)//si estamos minimizando el dominante es el que tenga menor Z
		{
			if(individuos_variable_j[i][num_var] < menor_z)
			{
				menor_z = individuos_variable_j[i][num_var];
				individuo_dominante = i;
			}
		}
		
		for(int j = 0; j < num_individuos; j++)
		{
			if(aleat_0_1 <= individuos_variable_j[j][num_var + 2])//ver en que rango cae el aleatorio
			{
				id_individuo = j;
				break;
			}
		}

		if(sobrevivientes.count(id_individuo) == 0)//ingresar los sobrevivientes a un map
		{
			num_sobrevivientes++;
			sobrevivientes[id_individuo] = 1;
		}

		else//si ya aparece incrementar coincidencia
			sobrevivientes[id_individuo]++;
	}

	return sobrevivientes;
}
//---------------------------------------------------------------------------------------------------------------------------------
//Funcion que mantiene los individuos sobrevivientes en la nueva iteracion, copia solamente sus variables aleatorias y crea de ellas sus v_j
void manten_estos_individuos(vector<vector<int> > &random_individuos_mutaciones, vector<vector<int> > random_individuos, int num_individuos, unordered_map<int, int> sobrevivientes, int num_var, vector<vector<double> > &individuos_variable_j_mutaciones, unordered_map<char,variable> vars)
{
	int id_indiv, cont = 0;

	for(auto s : sobrevivientes)
	{
		id_indiv = s.first;

		for(int j = 0; j < num_var; j++)
			random_individuos_mutaciones[cont][j] = random_individuos[id_indiv][j];		
		cont++;
	}

	for(int i = 0; i < cont; i++)
		genera_variables_j(i, random_individuos_mutaciones[i], individuos_variable_j_mutaciones, num_var, vars);
}
//---------------------------------------------------------------------------------------------------------------------------------
//Funcion que agrega los individuos restantes a partir de uno dominante, lo que se hace es modificar un solo bit del aleatorio de alguna de las variables del individuo dominante
//dicho nuevo individuo generado se generan sus v_j y se verifica que este nuevo individuo cumpla con todas las restricciones, si no se busca uno nuevo
void agrega_individuos_mutados(int num_mutaciones, int dominante, vector<vector<int> > &random_individuos_mutaciones, vector<vector<int> > random_individuos, int num_individuos, int num_var, unordered_map<char,variable> vars, vector<vector<double> > &individuos_variable_j_mutaciones, vector<restriccion> restricciones)
{
	int inicio = num_individuos - num_mutaciones;
	int random_variable, bits_genotipo, random_bit, bit, variable_mutada;
	char c, modifica_esta_variable;	

	int i = inicio;

	while(i < num_individuos)
	{
		for(int j = 0; j < num_var; j++)
			random_individuos_mutaciones[i][j] = random_individuos[dominante][j];

		c = 'a';
		random_variable = rand() % num_var;
		modifica_esta_variable = c + random_variable;
		bits_genotipo = vars[modifica_esta_variable].m;

		random_bit = rand() % bits_genotipo;
		bit = random_individuos_mutaciones[i][random_variable] & (1 << random_bit);//ver el estado del bit que intentamos cambiar

		if(bit == 0)//si el bit esta apagado entonces lo prendemos
		{
			variable_mutada = random_individuos_mutaciones[i][random_variable] | (1 << random_bit);
			random_individuos_mutaciones[i][random_variable] = variable_mutada;
		}

		else//si el bit esta prendido entonces lo apagamos
		{
			variable_mutada = random_individuos_mutaciones[i][random_variable] ^ (1 << random_bit);
			random_individuos_mutaciones[i][random_variable] = variable_mutada;
		}

		genera_variables_j(i, random_individuos_mutaciones[i], individuos_variable_j_mutaciones, num_var, vars);

		if(se_puede_tomar_individuo(individuos_variable_j_mutaciones[i], restricciones, num_var))//continua con las siguiente mutacion
			i++;
	}
}
//---------------------------------------------------------------------------------------------------------------------------------
//Funcion que imprime los valores aleatorios de los individuos y la tabla de resultados
void imprime(int num_individuos, int num_var, vector<vector<int> > random_individuos, vector<vector<double> > individuos_variable_j)
{
	cout << "---------------------------------------------------------------\n";

	for(int i = 0; i < num_individuos; i++)
	{
		cout << "(" << i << ") ";
		for(int j = 0; j < num_var; j++)
			cout << random_individuos[i][j] << " ";
		cout << endl;
	}

	cout << "---------------------------------------------------------------\n";

	for(int i = 0; i < num_individuos; i++)
	{
		cout << "(" << i << ") ";
		for(int j = 0; j < individuos_variable_j[i].size(); j++)
			cout << individuos_variable_j[i][j] << " ";
		cout << endl;
	}
}
//---------------------------------------------------------------------------------------------------------------------------------
int main()
{
	int num_var, bits, num_individuos, num_restricciones;
	double inf, sup, coeficiente, valor;
	double param;
	string signo, tipo;
	variable aux;
	restriccion aux2;
	bool max_min;

	srand(time(NULL));

	//--------------------------------------------------------------------------------------------
	cout << "Introduce el numero de variables: \n";
	cin >> num_var;
	//--------------------------------------------------------------------------------------------
	
	unordered_map<char,variable> vars;

	//El char c se usa para iterar sobre el unordered_map, ya que los nombres de las variables van en orden desde a hasta z
	char c = 'a';
	
	for (int i = 0; i < num_var; ++i, c++)
	{
		cout << "Introduzca el limite inferior y el superior para la variable " << c << " :\n";
		cin >> inf >> sup;
		aux.inferior = inf;
		aux.superior = sup;
		vars[c] = aux;
	}
	//--------------------------------------------------------------------------------------------
	cout << "Introduzca los bits de precision: \n";
	cin >> bits;
	//--------------------------------------------------------------------------------------------
	c = 'a';
	//Calculamos todos los bits de genotipo para cada variable
	for (int i = 0; i < num_var; ++i, c++)
	{
		param = (vars[c].superior - vars[c].inferior) * pow(10,bits);
		vars[c].m = ceil(log2(param));

		cout << "La variable " << c << " tendra un numero de " << vars[c].m <<" bits\n";
	}
	//--------------------------------------------------------------------------------------------
	cout << "Introduzca el numero de restricciones: \n";
	cin >> num_restricciones;
	
	vector<restriccion> restricciones(num_restricciones);
	//--------------------------------------------------------------------------------------------
	cout << "Inserte los coeficientes para cada variable segun la restriccion, despues ponga el la desigualdad ( >= o <= ) y al final el valor a comparar\n";
	vector<double> coeficientes(num_var);

	for (int i = 0; i < restricciones.size(); ++i)
	{
		for (int j = 0; j < num_var; ++j)
		{
			cin >> coeficiente;
			coeficientes[j] = coeficiente;
			aux2.coef = coeficientes;
		}

		cin >> signo;

		if(signo == ">=")
			aux2.signo = 1;

		else
			aux2.signo = 0;

		cin >> valor;
		aux2.igual = valor;
		restricciones[i] = aux2;
	}
	//--------------------------------------------------------------------------------------------
	cout << "Introduzca los coeficientes de la funcion: \n";
	vector<double> coeficientes_funcion(num_var);

	for(int i = 0; i < coeficientes_funcion.size(); i++)
	{
		cin >> coeficiente;
		coeficientes_funcion[i] = coeficiente;
	}
	//--------------------------------------------------------------------------------------------
	cout << "Quiere minimizar (min) o maximizar (max): \n";
	cin >> tipo;

	if(tipo == "min")
		max_min = false;
	if(tipo == "max")
		max_min = true;
	//--------------------------------------------------------------------------------------------
	cout << "Introduzca el numero de individuos: \n";
	cin >> num_individuos;
	//--------------------------------------------------------------------------------------------
	vector<int> aleatorios_variables(num_var, 0);
	vector<vector<int> > random_individuos(num_individuos, aleatorios_variables);
	
	vector<double> varible_j(num_var + 4, 0);
	vector<vector<double> > individuos_variable_j(num_individuos, varible_j);
	//-------------------------------------------------------------------------------------------------	
	genera_aleatorios_variables(random_individuos, num_individuos, vars, num_var, individuos_variable_j, restricciones);
	completa_matriz(individuos_variable_j, num_individuos, num_var, coeficientes_funcion);
	//-------------------------------------------------------------------------------------------------
	cout << "\nIteracion 1 " << endl;
	// imprime(num_individuos, num_var, random_individuos, individuos_variable_j);
	//-------------------------------------------------------------------------------------------------
	//repeticiones // id_individuo
	unordered_map<int, int> sobrevivientes;

	sobrevivientes = individuos_sobrevivientes(individuos_variable_j, num_individuos, num_var, max_min);
	int num_mutaciones = num_individuos - num_sobrevivientes;
	//--------------------------------------------------------------------------------------------
	vector<vector<int> > random_individuos_mutaciones(num_individuos, aleatorios_variables);
	vector<vector<double> > individuos_variable_j_mutaciones(num_individuos, varible_j);
	//-------------------------------------------------------------------------------------------------
	manten_estos_individuos(random_individuos_mutaciones, random_individuos, num_individuos, sobrevivientes, num_var, individuos_variable_j_mutaciones, vars);
	agrega_individuos_mutados(num_mutaciones, individuo_dominante, random_individuos_mutaciones, random_individuos, num_individuos, num_var, vars, individuos_variable_j_mutaciones, restricciones);
	completa_matriz(individuos_variable_j_mutaciones, num_individuos, num_var, coeficientes_funcion);
	//-------------------------------------------------------------------------------------------------
	vector<vector<int> > random_individuos_PRIMERA(num_individuos, aleatorios_variables);
	vector<vector<double> > individuos_variable_j_PRIMERA(num_individuos, varible_j);

	int iteracion = 2;
	//-------------------------------------------------------------------------------------------------
	random_individuos_PRIMERA = random_individuos_mutaciones;
	individuos_variable_j_PRIMERA = individuos_variable_j_mutaciones;
	//-------------------------------------------------------------------------------------------------

	while(iteracion < 101)
	{
		vector<vector<int> > random_individuos_SEGUNDA(num_individuos, aleatorios_variables);
		vector<vector<double> > individuos_variable_j_SEGUNDA(num_individuos, varible_j);

		cout << "\nIteracion " << iteracion <<  endl;
		// imprime(num_individuos, num_var, random_individuos_PRIMERA, individuos_variable_j_PRIMERA);

		unordered_map<int, int> sobrevivientes2;
		sobrevivientes2 = individuos_sobrevivientes(individuos_variable_j_PRIMERA, num_individuos, num_var, max_min);
		//dominante, individuos a usar (sobrevivientes2), num_sobrevientes

		int num_mutaciones = num_individuos - num_sobrevivientes;
		//-----------------------------------------------------------------------------------------------
		manten_estos_individuos(random_individuos_SEGUNDA, random_individuos_PRIMERA, num_individuos, sobrevivientes2, num_var, individuos_variable_j_SEGUNDA, vars);
		agrega_individuos_mutados(num_mutaciones, individuo_dominante, random_individuos_SEGUNDA, random_individuos_PRIMERA, num_individuos, num_var, vars, individuos_variable_j_SEGUNDA, restricciones);
		completa_matriz(individuos_variable_j_SEGUNDA, num_individuos, num_var, coeficientes_funcion);
		//-------------------------------------------------------------------------------------------------
		random_individuos_PRIMERA = random_individuos_SEGUNDA;
		individuos_variable_j_PRIMERA = individuos_variable_j_SEGUNDA;

		iteracion++;
	}

	// cout << "\n\nLA ULTIMA MATRIZ RESULTADOS ES" << endl;
	// imprime(num_individuos, num_var, random_individuos_PRIMERA, individuos_variable_j_PRIMERA);

	double max_z, min_z;
	int respuestas;

	if(max_min == true)
	{
		max_z = -1.0;
		respuestas = 0;

		for(int i = 0; i < num_individuos; i++)
		{
			if(individuos_variable_j_PRIMERA[i][num_var] > max_z)
			{
				max_z = individuos_variable_j_PRIMERA[i][num_var];
				respuestas = i;
			}
		}
	}

	if(max_min == false)
	{
		min_z = 1000000.0;
		respuestas = 0;

		for(int i = 0; i < num_individuos; i++)
		{
			if(individuos_variable_j_PRIMERA[i][num_var] < min_z)
			{
				min_z = individuos_variable_j_PRIMERA[i][num_var];
				respuestas = i;
			}
		}
	}

	cout << "las respuestas son \n\n";

	for(int i = 0; i <= num_var; i++)
		cout << individuos_variable_j_PRIMERA[respuestas][i] << " ";

	
	return 0;
}

/*
	Test cases:

	2
	0 3
	1 5
	1
	4
	1 0 >= 0
	0 1 >= 1
	1 0 <= 3
	0 1 <= 5
	1 2
	1000

	MAX 3 5 13
	MIN 0 1 2
		

	2
	0 12.5
	0 12.5
	1
	5
	4 3 <= 30
	2 2 <= 25
	1 0 >= 3
	0 1 >= 0
	1 0 >= 0
	2 5
	1000

	MAX 3 6 36
	MIN 3 0 6


	2
	0 25
	0 10
	1
	5
	1 3 <= 25
	2 5 >= 3
	1 2 <= 20
	1 0 >= 0
	0 1 >= 0
	2 2
	1000

	MAX 20 0 40
	MIN 0 0.6 1.2

	2
	0 20
	0 20
	1
	4
	2 2 <= 35
	1 1 <= 20
	1 0 >= 0
	0 1 >= 0
	1 1
	1000

	MAX 0 17.5 17.5
	MIN 0 0 0 

	2
	0 17.5
	0 17.5
	1
	5
	1 3 >= 15
	2 2 <= 35
	1 0 >= 2
	0 1 >= 0
	1 0 >= 0
	2 3
	1000

	MAX 2 15.5 50.5
	MIN 2 4.33 17

	3
	0 300
	0 240
	0 150
	1
	6
	2 1 3 <= 180
	1 3 2 <= 300
	2 1 2 <= 240
	1 0 0 >= 0
	0 1 0 >= 0
	0 0 1 >= 0
	6 5 4
	1000

	MAX 48 84 0 708
	MIN 0 0 0 0

	-------------------------------

	2
	0 10
	0 20
	1
	4
	2 1 <= 20
	1 1 >= 10
	1 0 >= 0
	0 1 >= 0
	1 1
	1000

	-------------------------------

	3
	0 50
	0 75
	-5 50
	1
	7
	1 0 1 <= 50
	2 1 0 <= 75
	1 0 -1 >= 10
	1 0 0 >= 0
	0 1 0 >= 0
	0 0 1 >= 0
	0 0 1 >= -5
	1 1 1

	---------------------------------
	4
	0 30
	0 30
	0 100
	0 40
	1
	13
	1 0 0 0 >= 0
	0 1 0 0 >= 0
	0 0 1 0 >= 0
	0 0 0 1 >= 0
	1 1 0 0 <= 30
	1 0 0 1 <= 40
	0 0 1 1 <= 70
	0 1 1 0 <= 60
	1 0 0 0 <= 30
	0 1 0 0 <= 30
	0 0 1 0 <= 100
	0 0 0 1 <= 40
	1 1 1 1 >= 98
	1 -1 1 1


	4
	0 30
	0 30
	0 100
	0 40
	1
	9
	1 0 0 0 >= 0
	0 1 0 0 >= 0
	0 0 1 0 >= 0
	0 0 0 1 >= 0
	1 1 0 0 <= 30
	1 0 0 1 <= 40
	0 0 1 1 <= 70
	0 1 1 0 <= 60
	1 1 1 1 >= 98
	1 -1 1 1

	
	-----------------------
	4
	0 50
	0 100
	0 100
	0 50
	1
	9
	1 0 0 1 <= 50
	0 1 1 0 <= 75
	1 0 0 0 >= 10
	0 1 1 0 <= 100
	0 0 1 2 >= 30
	1 0 0 0 >= 0
	0 1 0 0 >= 0
	0 0 1 0 >= 0
	0 0 0 1 >= 0
	1 1 1 -2



	4
	0 50
	0 75
	0 75
	0 50
	1
	9
	1 0 0 1 <= 50
	0 1 1 0 <= 75
	1 0 0 0 >= 10
	0 1 1 0 <= 100
	0 0 1 2 >= 30
	1 0 0 0 >= 0
	0 1 0 0 >= 0
	0 0 1 0 >= 0
	0 0 0 1 >= 0
	1 1 1 -2



*/
