#include <bits/stdc++.h>
using namespace std;
				#define python_level_type_first int
				#define python_level_type_second int
				#define convert_first_type to_string
				std::vector<std::unordered_map<python_level_type_first,python_level_type_second*>> python_globals;
				std::vector<std::unordered_map<python_level_type_first,python_level_type_second>*> python_locals_pointers;
				#define python_global(q)\
				 	if (!python_globals[0].count(q)){\
						(*(python_locals_pointers[0]))[q]=int64_t(0);\
						python_globals[0][q]=&((*(python_locals_pointers[0]))[q]);\
					}\
					python_globals[python_globals.size()-1][q]=python_globals[0][q];

				#define python_nonlocal(q)\
				 	if (!python_globals[python_globals.size()-2].count(q)){\
						(*(python_locals_pointers[python_locals_pointers.size()-2]))[q]=int64_t(0);\
						python_globals[python_globals.size()-2][q]=&((*(python_locals_pointers[python_locals_pointers.size()-2]))[q]);\
					}\
					python_globals[python_globals.size()-1][q]=python_globals[python_globals.size()-2][q];
					
				python_level_type_second& python_level_get(python_level_type_first q){
					for (int64_t w=python_globals.size()-1;w>=0;--w){
						if (python_globals[w].count(q)){
							return *(python_globals[w][q]);
						}
					}
					std::cout<<std::string("name ")+convert_first_type(q)+std::string(" is undefined")<<std::endl;
					return *(python_globals[0][q]);
				}

				bool __python__isdefined(python_level_type_first q){
					for (auto w=python_globals.size()-1;w>=0;--w){
						if (python_globals[w].count(q)){
							return true;
						}
					}
					return false;
				}

				python_level_type_second& python_level_set(python_level_type_first q){
					if (!python_globals[python_globals.size()-1].count(q)) {
						(*(python_locals_pointers[python_locals_pointers.size()-1]))[q]=int64_t(0);
						python_globals[python_globals.size()-1][q]=&((*(python_locals_pointers[python_locals_pointers.size()-1]))[q]);
					}
					return *(python_globals[python_globals.size()-1][q]);
				}

				#define python_create_level()\
					python_globals.emplace_back();\
					std::unordered_map<python_level_type_first,python_level_type_second> python_locals;\
					python_locals_pointers.push_back(&python_locals);

				#define python_delete_level()\
					python_globals.pop_back();\
					python_locals_pointers.pop_back();

int main(){
	python_create_level()

	python_level_set(1)=10;
	python_level_set(2)=20;
	python_level_set(3)=30;
	python_level_set(4)=40;

	// cout<<python_level_get(1)<<endl;

	{
		python_create_level()

		python_level_set(1)=11;
		python_level_set(2)=21;
		python_level_set(3)=31;
		python_level_set(4)=41;

		{
			python_create_level()

			python_level_set(1)=12;
			python_level_set(2)=22;
			python_level_set(3)=32;
			python_level_set(4)=42;

			{
				python_create_level()

				python_nonlocal(3)

				python_level_set(1)=13;
				// python_level_set(2)=23;
				python_level_set(3)=33;
				python_level_set(4)=43;

				{
					python_create_level()

					python_global(1)
					python_nonlocal(2)
					python_nonlocal(3)

					python_level_set(1)=14;
					python_level_set(2)=24;
					python_level_set(3)=34;
					python_level_set(4)=44;

					cout<<python_level_get(1)<<endl;
					cout<<python_level_get(2)<<endl;
					cout<<python_level_get(3)<<endl;
					cout<<python_level_get(4)<<endl;
					// cout<<python_level_get(5)<<endl;
					cout<<"--"<<endl;

					python_delete_level()
				}

				cout<<python_level_get(1)<<endl;
				cout<<python_level_get(2)<<endl;
				cout<<python_level_get(3)<<endl;
				cout<<python_level_get(4)<<endl;
				cout<<"--"<<endl;

				python_delete_level()
			}
			cout<<python_level_get(1)<<endl;
			cout<<python_level_get(2)<<endl;
			cout<<python_level_get(3)<<endl;
			cout<<python_level_get(4)<<endl;
			cout<<"--"<<endl;
			python_delete_level()
		}
		cout<<python_level_get(1)<<endl;
		cout<<python_level_get(2)<<endl;
		cout<<python_level_get(3)<<endl;
		cout<<python_level_get(4)<<endl;
		cout<<"--"<<endl;
		python_delete_level()
	}
	cout<<python_level_get(1)<<endl;
	cout<<python_level_get(2)<<endl;
	cout<<python_level_get(3)<<endl;
	cout<<python_level_get(4)<<endl;
	cout<<"--"<<endl;
	python_delete_level()

	
	
	// for(python_level_set(5):vector<int>({1,2,3,4,5})){
	// 	cout<<python_level_get(5)<<endl;
	// }
}