# A simple implementation of hard-to-vary

This is my submission for [Veritula's bounty for Idea #3069](https://veritula.com/bounties/8), which asks for an executable implementation that can compare arbitrary English explanations by how hard they are to vary.

**Code:** [htv.py](./htv.py)

I've implemented the approach as a small interactive program. It takes arbitrary explanations supplied by the user, collects working variations of each, and ranks the explanations by hardness to vary.

I think hard-to-vary can be implemented more simply than the approaches considered in Dennis's blog, [*Hard to Vary or Hardly Usable?*](https://blog.dennishackethal.com/posts/hard-to-vary-or-hardly-usable). The basic idea I'm using is this: if an explanation is harder to vary, there should be fewer ways of changing it while still having it explain what it's supposed to explain.

The program starts by asking the user what question they're trying to answer and then asks for a list of proposed explanations. It goes through each explanation one at a time and asks the user to come up with variations of it that would still work as explanations. The user can enter as many as they can find, then move on to the next explanation.

Finally, the program counts the working variations and ranks the explanations. Fewer working variations means harder to vary, while equal numbers mean equally hard to vary. So if explanation A has two working variations and explanation B has five, A is harder to vary than B.

## An example

Take the question: **Why do seasons occur?**

One explanation is the story of Persephone. She spends part of the year in Hades, Demeter grieves while she's gone, and this accounts for the seasonal cycle.

I might try changing the explanation in a few ways:

- Persephone spends five months in Hades instead of six.
- It's Demeter's son who is taken rather than her daughter.
- Zeus orders Persephone to return periodically rather than her return depending on the details involving the pomegranate.

The details have changed, but the basic explanatory story can still do the same job. Suppose I find three such variations.

Now I try the explanation involving Earth's axial tilt. I might be able to change the stated tilt from 23.4 degrees to 23.5 degrees without substantially affecting the explanation. But if I start making large changes to the geometry while trying to explain the same observations, the explanation stops working. Suppose I find one working variation.

The program therefore ranks axial tilt as harder to vary: one working variation versus three. That's the entire comparison procedure.

## How I understand Dennis's criticism

I don't understand Dennis as claiming that Deutsch simply gets the Persephone example wrong. The issue in the blog is how we get from examples like this, where we seem to have an intuition that one explanation is harder to vary, to a sufficiently specified procedure that could compare explanations in general.

Dennis initially explores numerical quality scores, but that immediately creates problems. Why should one explanation have a score of 500 rather than 550? Why choose that scale? How do criticisms affect the score? How do criticisms of criticisms affect it? I agree with Dennis that these choices look arbitrary.

He eventually gets rid of the quality scores entirely. Instead of trying to measure the quality of an idea, his program keeps track of pending criticisms. His proposed rule becomes: adopt ideas without pending criticisms and reject ideas that have them.

There's something important about how that system works, though. The program doesn't generate criticisms itself; people do. And that's intentional: Dennis says "I’m not looking to formalize or automate *creativity as a whole*". Creative input can come from users while the program handles the non-creative part of the process. I agree that you can have a rational decision-making process while outsourcing the creative part to the user.

I just don't see why we can't do the same thing with HTV. Let the user come up with variations and say which ones they think still work. The program doesn't need to understand the explanation or come up with the variations itself. It keeps track of the variations and compares the counts.

This doesn't seem fundamentally different from Dennis letting the user tell his program that something is a criticism. In fact, in the blog he explicitly avoids having the program figure out whether a comment is really a criticism: the user checks a box saying that it is. So in my program the user is supplying a working variation; in his, the user is supplying a criticism. In both cases the user is providing the part that requires understanding and judgment, and the program does something simple with that input.

It also means I don't need the quality scores Dennis runs into trouble with. I don't need to decide how many points axial tilt gets compared with Persephone. I'm just asking: how many ways have we actually found to change each explanation while still having it work?

## But isn't this subjective?

One criticism Dennis quotes is:

> “Also, isn’t the difficulty of changing an explanation at least partly a property not of the explanation itself but of whoever is trying to change it? If I’m having difficulty changing it, maybe that’s because I lack imagination. Or maybe I’m just new to that field and an expert could easily change it.”

I think this is true. I just don't think it's a problem specific to HTV.

Imagine I can't think of any working variations of an explanation, but an expert can immediately think of five. Then yes, our results will be different. But isn't that also what happens with criticism? I might look at an idea and fail to see anything wrong with it while someone who knows much more about the subject immediately sees a serious criticism.

The same goes for participation. An idea on Veritula might have zero pending criticisms simply because hardly anyone has tried to criticize it. That doesn't mean there are literally no criticisms of it. Someone could find one tomorrow. Dennis's answer in the blog is basically that if this bothers you, try to find a criticism yourself. If you can't find one, why not adopt the idea?

I think HTV can work the same way. Zero working variations doesn't mean that we've somehow proven there are no possible variations. It means we haven't found one. If you think the explanation is actually easy to vary, try to come up with a variation that still works.

So yes, the result depends on the knowledge and creativity of the person using the program. But I think rational decision-making is always going to depend on what criticisms, arguments, alternatives, etc. a person is actually aware of. I don't see how Veritula escapes that either.

## What about human judgment?

There's another obvious question: who decides whether a variation actually works?

For this program, the user does. I don't think we can get rid of that kind of human judgment, at least until we get AGI. Two people can disagree about whether a variation still explains the thing we're trying to explain. They can also disagree about whether two variations are really different or are basically the same variation stated twice.

Again, I think Veritula has the same underlying issue. People still have to decide whether something really is a criticism, whether a countercriticism actually answers it, whether two criticisms are redundant, and so on. Dennis's program can keep track of the structure, but the structure only means something if those judgments make sense.

Take an extreme case. If a malicious moderator rejects every good criticism of an idea and accepts nonsense countercriticisms, the idea could end up showing `0 pending criticisms`. I obviously shouldn't look at the `0` and conclude that the idea is rational to adopt. I'd want to read what happened and decide whether I agree with it.

I don't mean this as a criticism specific to Veritula. I think it's just a limit of this kind of approach. At some point people have to make judgments, and people can disagree about them. Ultimately everyone is their own moderator when it comes to their own decision-making. I have to decide which arguments I accept, which criticisms I think have been answered, and so on.

The same is true with my HTV program. If someone gives me a ranking based on ten supposed working variations, I don't have to accept the ranking blindly. I can look at the ten variations and decide that five don't really work and three others are basically duplicates. My result would then be different.

I'm fine with that. I don't think the goal of either program should be to somehow remove judgment from rational thinking. The program gives us a procedure for what to do with the judgments we've made.

## What does the program actually contribute?

Dennis writes:

> “We can’t just outsource *everything* to the user – the app has to do *some* things or it has no value.”

This was actually the part of the blog that made me think about Veritula itself. What is Veritula doing, and what is it outsourcing?

It outsources the interesting creative part to people. People come up with the ideas. People come up with the criticisms. The user can even tell the program whether something they've written is a criticism by checking a box. The program then keeps track of the structure and tells us how many criticisms are pending.

My program is doing something similar, except with variations. People come up with the explanations and the working variations. The program keeps track of them, counts them, and ranks the explanations.

So I don't think I'm outsourcing everything to the user any more than Veritula is. I'm outsourcing the part that requires creativity and judgment. The actual decision rule is implemented in the program.

For Veritula, that rule ultimately depends on whether there are pending criticisms. For my program, it depends on the number of working variations: fewer working variations means harder to vary.

## Where I disagree with the blog

I agree with Dennis that the quality sliders in the blog don't work. I also agree with his decision to let users supply the creative input rather than expecting the program to generate it.

Where I disagree is that I think once we allow this same freedom for HTV, we can construct a similarly simple program for it. The user comes up with explanations and tries to vary them while keeping them working. The program counts the working variations and ranks the explanations.

There are still all the normal problems of human knowledge: maybe I missed a variation, maybe I accepted a bad one, maybe someone else would judge things differently. But those same problems exist when we come up with and judge criticisms.

I don't think either program solves those problems, and I don't think it needs to. That's the part people do.
