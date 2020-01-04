#include <stdio.h>
#include <inttypes.h>

#define uint128_t unsigned __int128
#define int128_t __int128

uint128_t card = 2020;
uint128_t lenstack = 119315717514047;
uint128_t tot = 101741582076661;

/*
uint128_t card = 2019;
uint128_t lenstack = 10007;
uint128_t tot = 1;
*/

void deal()
{
    card = lenstack - card - 1LL;
}

void cut(int128_t i)
{
    if (i < 0)
        i = lenstack + i;
    if (card < i)
        card += (lenstack - i);
    else
        card -= i;
}

void incr(int i)
{
    card = (card * (uint128_t)i) % lenstack;
}

int main()
{
    for (uint128_t i = 0; i < tot; i++)
    {
        cut(4913);
        incr(53);
        cut(-1034);
        deal();
        incr(49);
        deal();
        cut(-7153);
        incr(59);
        cut(4618);
        incr(15);
        cut(-8047);
        incr(67);
        cut(9890);
        incr(16);
        cut(-870);
        incr(34);
        cut(-4557);
        incr(19);
        cut(-6466);
        incr(47);
        cut(-5860);
        incr(65);
        deal();
        cut(-8104);
        incr(15);
        cut(-9013);
        deal();
        cut(7309);
        incr(36);
        deal();
        cut(-1340);
        incr(42);
        cut(-5204);
        incr(75);
        deal();
        incr(16);
        deal();
        incr(44);
        cut(6833);
        incr(14);
        deal();
        cut(2345);
        incr(60);
        cut(4830);
        incr(75);
        cut(-2843);
        incr(50);
        cut(3816);
        deal();
        cut(7340);
        incr(48);
        cut(-3452);
        incr(62);
        cut(-2433);
        incr(59);
        cut(-4176);
        deal();
        cut(9365);
        incr(65);
        cut(-7815);
        incr(65);
        cut(5177);
        deal();
        incr(8);
        cut(-3200);
        incr(63);
        cut(-9460);
        incr(20);
        cut(-6926);
        incr(4);
        cut(-9863);
        incr(38);
        cut(-4295);
        incr(31);
        deal();
        cut(-9590);
        incr(22);
        cut(-9805);
        incr(48);
        deal();
        cut(-2326);
        incr(72);
        deal();
        incr(7);
        cut(-453);
        incr(15);
        cut(-7639);
        deal();
        incr(61);
        cut(-7303);
        incr(24);
        cut(4827);
        incr(48);
        cut(-1821);
        incr(31);
        cut(-9410);
        incr(5);
        cut(-2492);
        incr(25);
        cut(1313);

        if (i > 0 && i % 10000000 == 0)
        {
            printf("at %" PRIu64 "  %f\n", (uint64_t)i, i / tot);
            fflush(stdout);
            return 0;
        }
    }

    printf("card = %" PRIu64 "\n", (uint64_t)card);
}