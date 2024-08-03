for testname in $(
	for test in tests/*
	do echo $test | tr "/" "."
	done
)
do echo -e "\033[0;34m$testname\033[0m" && python3 -m ${testname//.py/} >/dev/null
done
